from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.responses import StreamingResponse
from app.database import SessionLocal
from app.models.arrival_act import ArrivalAct
from app.models.order import Order
from app.models.exhibit import Exhibit
from app.services.pdf_service import render_arrival_act_pdf_html, html_to_pdf

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/arrival_acts", name="arrival_acts_list")
def arrival_acts_list(request: Request, db: Session = Depends(get_db)):
    acts = db.query(ArrivalAct).all()
    return templates.TemplateResponse("arrival_acts/list.html", {"request": request, "acts": acts})

@router.get("/arrival_acts/create", name="arrival_acts_create_form")
def arrival_acts_create_form(request: Request, db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    exhibits = db.query(Exhibit).all()
    return templates.TemplateResponse(
        "arrival_acts/create.html",
        {"request": request, "orders": orders, "exhibits": exhibits}
    )

@router.post("/arrival_acts/create", name="arrival_acts_create")
def arrival_acts_create(
    order_id: int = Form(...),
    selected_exhibits: list[int] = Form([]),
    db: Session = Depends(get_db)
):
    act = ArrivalAct(order_id=order_id)
    db.add(act)
    db.commit()
    db.refresh(act)

    for ex_id in selected_exhibits:
        exhibit = db.query(Exhibit).get(ex_id)
        if exhibit:
            act.exhibits.append(exhibit)
    db.commit()

    return RedirectResponse(url="/arrival_acts", status_code=303)

@router.get("/arrival_acts/{act_id}", name="arrival_acts_detail")
def arrival_acts_detail(act_id: int, request: Request, db: Session = Depends(get_db)):
    act = db.query(ArrivalAct).get(act_id)
    if not act:
        return RedirectResponse(url="/arrival_acts", status_code=303)
    return templates.TemplateResponse("arrival_acts/detail.html", {"request": request, "act": act})

@router.get("/arrival_acts/{act_id}/edit", name="arrival_acts_edit_form")
def arrival_acts_edit_form(act_id: int, request: Request, db: Session = Depends(get_db)):
    act = db.query(ArrivalAct).get(act_id)
    if not act:
        return RedirectResponse(url="/arrival_acts", status_code=303)
    orders = db.query(Order).all()
    exhibits = db.query(Exhibit).all()
    return templates.TemplateResponse(
        "arrival_acts/edit.html",
        {"request": request, "act": act, "orders": orders, "exhibits": exhibits}
    )

@router.post("/arrival_acts/{act_id}/edit", name="arrival_acts_edit")
def arrival_acts_edit(
    act_id: int,
    order_id: int = Form(...),
    selected_exhibits: list[int] = Form([]),
    db: Session = Depends(get_db)
):
    act = db.query(ArrivalAct).get(act_id)
    if not act:
        return RedirectResponse(url="/arrival_acts", status_code=303)

    act.order_id = order_id
    # пересоздаём связь
    act.exhibits.clear()
    db.commit()

    for ex_id in selected_exhibits:
        exhibit = db.query(Exhibit).get(ex_id)
        if exhibit:
            act.exhibits.append(exhibit)

    db.commit()
    return RedirectResponse(url=f"/arrival_acts/{act_id}", status_code=303)

@router.post("/arrival_acts/{act_id}/delete", name="arrival_acts_delete")
def arrival_acts_delete(act_id: int, db: Session = Depends(get_db)):
    act = db.query(ArrivalAct).get(act_id)
    if act:
        db.delete(act)
        db.commit()
    return RedirectResponse(url="/arrival_acts", status_code=303)

@router.get("/arrival_acts/{act_id}/pdf", name="arrival_act_pdf")
def arrival_act_pdf(act_id: int, db: Session = Depends(get_db)):
    act = db.query(ArrivalAct).get(act_id)
    if not act:
        raise HTTPException(status_code=404, detail="Акт поступления не найден")

    html_str = render_arrival_act_pdf_html(act)
    pdf_io = html_to_pdf(html_str)

    filename = f"arrival_act_{act_id}.pdf"
    headers = {
        "Content-Disposition": f"attachment; filename={filename}"
    }
    return StreamingResponse(pdf_io, media_type="application/pdf", headers=headers)