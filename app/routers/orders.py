from io import BytesIO

from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, date

from fastapi.responses import StreamingResponse

from app.database import SessionLocal
from app.models.order import Order
from app.models.exhibition import Exhibition
from app.models.exhibit import Exhibit
from app.services.orders_service import calculate_stage
from app.services.pdf_service import render_order_pdf_html, html_to_pdf

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/orders", name="orders_list")
def orders_list(request: Request, db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return templates.TemplateResponse("orders/list.html", {"request": request, "orders": orders})


@router.get("/orders/create", name="orders_create_form")
def orders_create_form(request: Request, db: Session = Depends(get_db)):
    exhibitions = db.query(Exhibition).all()
    exhibits = db.query(Exhibit).all()
    return templates.TemplateResponse(
        "orders/create.html",
        {"request": request, "exhibitions": exhibitions, "exhibits": exhibits}
    )


@router.post("/orders/create", name="orders_create")
def orders_create(
        exhibition_id: int = Form(...),
        start_date: str = Form(...),
        end_date: str = Form(...),
        venue: str = Form(""),
        selected_exhibits: list[int] = Form([]),
        db: Session = Depends(get_db)
):
    sd = date.fromisoformat(start_date)
    ed = date.fromisoformat(end_date)

    order = Order(
        exhibition_id=exhibition_id,
        start_date=sd,
        end_date=ed,
        venue=venue
    )
    db.add(order)
    db.commit()

    if selected_exhibits:
        db.refresh(order)
        for ex_id in selected_exhibits:
            exhibit = db.query(Exhibit).get(ex_id)
            if exhibit:
                order.exhibits.append(exhibit)
        db.commit()

    return RedirectResponse(url="/orders", status_code=303)


@router.get("/orders/{order_id}", name="orders_detail")
def orders_detail(order_id: int, request: Request, db: Session = Depends(get_db)):
    order = db.query(Order).get(order_id)
    if not order:
        return RedirectResponse(url="/orders", status_code=303)

    stage = calculate_stage(order, db)
    return templates.TemplateResponse(
        "orders/detail.html",
        {
            "request": request,
            "order": order,
            "stage": stage
        }
    )
@router.get("/orders/{order_id}/edit", name="orders_edit_form")
def orders_edit_form(order_id: int, request: Request, db: Session = Depends(get_db)):
    order = db.query(Order).get(order_id)
    if not order:
        return RedirectResponse(url="/orders", status_code=303)

    exhibitions = db.query(Exhibition).all()
    exhibits = db.query(Exhibit).all()
    return templates.TemplateResponse(
        "orders/edit.html",
        {
            "request": request,
            "order": order,
            "exhibitions": exhibitions,
            "exhibits": exhibits
        }
    )


@router.post("/orders/{order_id}/edit", name="orders_edit")
def orders_edit(
        order_id: int,
        exhibition_id: int = Form(...),
        start_date: str = Form(...),
        end_date: str = Form(...),
        venue: str = Form(""),
        selected_exhibits: list[int] = Form([]),
        db: Session = Depends(get_db)
):
    order = db.query(Order).get(order_id)
    if not order:
        return RedirectResponse(url="/orders", status_code=303)

    sd = date.fromisoformat(start_date)
    ed = date.fromisoformat(end_date)

    order.exhibition_id = exhibition_id
    order.start_date = sd
    order.end_date = ed
    order.venue = venue

    order.exhibits.clear()
    db.commit()

    for ex_id in selected_exhibits:
        exhibit = db.query(Exhibit).get(ex_id)
        if exhibit:
            order.exhibits.append(exhibit)

    db.commit()
    return RedirectResponse(url=f"/orders/{order_id}", status_code=303)


@router.post("/orders/{order_id}/delete", name="orders_delete")
def orders_delete(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).get(order_id)
    if order:
        db.delete(order)
        db.commit()
    return RedirectResponse(url="/orders", status_code=303)
@router.get("/orders/{order_id}/pdf", name="order_pdf")
def order_pdf(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Приказ не найден")

    html_str = render_order_pdf_html(order)
    pdf_io = html_to_pdf(html_str)

    filename = f"order_{order_id}.pdf"
    headers = {
        "Content-Disposition": f"attachment; filename={filename}"
    }
    return StreamingResponse(pdf_io, media_type="application/pdf", headers=headers)