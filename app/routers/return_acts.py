from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime, date
from fastapi.responses import StreamingResponse
from app.database import SessionLocal
from app.models.return_act import ReturnAct
from app.models.order import Order
from app.models.exhibit import Exhibit
from app.models.transfer_act import TransferAct
from app.services.pdf_service import render_return_act_pdf_html, html_to_pdf

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/return_acts", name="return_acts_list")
def return_acts_list(request: Request, db: Session = Depends(get_db)):
    acts = db.query(ReturnAct).all()
    return templates.TemplateResponse("return_acts/list.html", {"request": request, "acts": acts})

@router.get("/return_acts/create", name="return_acts_create_form")
def return_acts_create_form(request: Request, db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    exhibits = db.query(Exhibit).all()
    return templates.TemplateResponse(
        "return_acts/create.html",
        {"request": request, "orders": orders, "exhibits": exhibits}
    )

@router.post("/return_acts/create", name="return_acts_create")
def return_acts_create(
    order_id: int = Form(...),
    selected_exhibits: list[int] = Form([]),
    db = Depends(get_db)
):
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=400, detail="Приказа не существует")

    # Проверим, закончилась ли выставка:
    if order.end_date > date.today():
        raise HTTPException(status_code=400, detail="Выставка ещё не закончилась.")

    # Проверим, что все выбранные экспонаты «переданы»
    transfer_acts_for_order = db.query(TransferAct).filter(TransferAct.order_id == order_id).all()
    transferred_exhibit_ids = set()
    for t_act in transfer_acts_for_order:
        for ex in t_act.exhibits:
            transferred_exhibit_ids.add(ex.id)

    for ex_id in selected_exhibits:
        if ex_id not in transferred_exhibit_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Экспонат ID={ex_id} не был передан (невозможно вернуть)."
            )

    # Если всё ок, создаём ReturnAct
    act = ReturnAct(order_id=order_id)
    db.add(act)
    db.commit()
    db.refresh(act)

    for ex_id in selected_exhibits:
        exhibit = db.query(Exhibit).get(ex_id)
        if exhibit:
            act.exhibits.append(exhibit)

    db.commit()
    return RedirectResponse(url="/return_acts", status_code=303)

@router.get("/return_acts/{act_id}", name="return_acts_detail")
def return_acts_detail(act_id: int, request: Request, db: Session = Depends(get_db)):
    act = db.query(ReturnAct).get(act_id)
    if not act:
        return RedirectResponse(url="/return_acts", status_code=303)
    return templates.TemplateResponse("return_acts/detail.html", {"request": request, "act": act})

@router.get("/return_acts/{act_id}/edit", name="return_acts_edit_form")
def return_acts_edit_form(act_id: int, request: Request, db: Session = Depends(get_db)):
    act = db.query(ReturnAct).get(act_id)
    if not act:
        return RedirectResponse(url="/return_acts", status_code=303)
    orders = db.query(Order).all()
    exhibits = db.query(Exhibit).all()
    return templates.TemplateResponse(
        "return_acts/edit.html",
        {"request": request, "act": act, "orders": orders, "exhibits": exhibits}
    )

@router.post("/return_acts/{act_id}/edit", name="return_acts_edit")
def return_acts_edit(
    act_id: int,
    order_id: int = Form(...),
    selected_exhibits: list[int] = Form([]),
    db: Session = Depends(get_db)
):
    act = db.query(ReturnAct).get(act_id)
    if not act:
        return RedirectResponse(url="/return_acts", status_code=303)

    act.order_id = order_id
    act.exhibits.clear()
    db.commit()

    for ex_id in selected_exhibits:
        exhibit = db.query(Exhibit).get(ex_id)
        if exhibit:
            act.exhibits.append(exhibit)

    db.commit()
    return RedirectResponse(url=f"/return_acts/{act_id}", status_code=303)

@router.post("/return_acts/{act_id}/delete", name="return_acts_delete")
def return_acts_delete(act_id: int, db: Session = Depends(get_db)):
    act = db.query(ReturnAct).get(act_id)
    if act:
        db.delete(act)
        db.commit()
    return RedirectResponse(url="/return_acts", status_code=303)

@router.get("/return_acts/{act_id}/pdf", name="return_act_pdf")
def return_act_pdf(act_id: int, db: Session = Depends(get_db)):
    act = db.query(ReturnAct).get(act_id)
    if not act:
        raise HTTPException(status_code=404, detail="Акт возврата не найден")

    html_str = render_return_act_pdf_html(act)
    pdf_io = html_to_pdf(html_str)

    filename = f"return_act_{act_id}.pdf"
    headers = {
        "Content-Disposition": f"attachment; filename={filename}"
    }
    return StreamingResponse(pdf_io, media_type="application/pdf", headers=headers)