from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime
from fastapi.responses import StreamingResponse

from app.database import SessionLocal
from app.models.arrival_act import ArrivalAct
from app.models.transfer_act import TransferAct
from app.models.order import Order
from app.models.exhibit import Exhibit
from app.services.pdf_service import render_transfer_act_pdf_html, html_to_pdf

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/transfer_acts", name="transfer_acts_list")
def transfer_acts_list(request: Request, db: Session = Depends(get_db)):
    acts = db.query(TransferAct).all()
    return templates.TemplateResponse("transfer_acts/list.html", {"request": request, "acts": acts})

@router.get("/transfer_acts/create", name="transfer_acts_create_form")
def transfer_acts_create_form(request: Request, db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    exhibits = db.query(Exhibit).all()
    return templates.TemplateResponse(
        "transfer_acts/create.html",
        {"request": request, "orders": orders, "exhibits": exhibits}
    )

@router.post("/transfer_acts/create", name="transfer_acts_create")
def transfer_acts_create(
    order_id: int = Form(...),
    selected_exhibits: list[int] = Form([]),
    db: Session = Depends(get_db)
):
    order = db.query(Order).get(order_id)
    if not order:
        raise HTTPException(status_code=400, detail="Приказа не существует")

    today = datetime.now().date()
    if not (order.start_date <= today <= order.end_date):
        raise HTTPException(
            status_code=400,
            detail="Перемещение экспонатов вне периода проведения выставки запрещено."
        )


    arrival_acts_for_order = db.query(ArrivalAct).filter(ArrivalAct.order_id == order_id).all()
    arrived_exhibit_ids = set()
    for arrival_act in arrival_acts_for_order:
        for ex in arrival_act.exhibits:
            arrived_exhibit_ids.add(ex.id)

    for ex_id in selected_exhibits:
        if ex_id not in arrived_exhibit_ids:
            raise HTTPException(
                status_code=400,
                detail=f"Экспонат ID={ex_id} ещё ене прибыл. Невозможно переместить."
            )

    act = TransferAct(order_id=order_id)
    db.add(act)
    db.commit()
    db.refresh(act)

    for ex_id in selected_exhibits:
        exhibit = db.query(Exhibit).get(ex_id)
        if exhibit:
            act.exhibits.append(exhibit)

    db.commit()
    return RedirectResponse(url="/transfer_acts", status_code=303)
@router.get("/transfer_acts/{act_id}", name="transfer_acts_detail")
def transfer_acts_detail(act_id: int, request: Request, db: Session = Depends(get_db)):
    act = db.query(TransferAct).get(act_id)
    if not act:
        return RedirectResponse(url="/transfer_acts", status_code=303)
    return templates.TemplateResponse("transfer_acts/detail.html", {"request": request, "act": act})

@router.get("/transfer_acts/{act_id}/edit", name="transfer_acts_edit_form")
def transfer_acts_edit_form(act_id: int, request: Request, db: Session = Depends(get_db)):
    act = db.query(TransferAct).get(act_id)
    if not act:
        return RedirectResponse(url="/transfer_acts", status_code=303)
    orders = db.query(Order).all()
    exhibits = db.query(Exhibit).all()
    return templates.TemplateResponse(
        "transfer_acts/edit.html",
        {"request": request, "act": act, "orders": orders, "exhibits": exhibits}
    )

@router.post("/transfer_acts/{act_id}/edit", name="transfer_acts_edit")
def transfer_acts_edit(
    act_id: int,
    order_id: int = Form(...),
    selected_exhibits: list[int] = Form([]),
    db: Session = Depends(get_db)
):
    act = db.query(TransferAct).get(act_id)
    if not act:
        return RedirectResponse(url="/transfer_acts", status_code=303)

    act.order_id = order_id
    act.exhibits.clear()
    db.commit()

    for ex_id in selected_exhibits:
        exhibit = db.query(Exhibit).get(ex_id)
        if exhibit:
            act.exhibits.append(exhibit)

    db.commit()
    return RedirectResponse(url=f"/transfer_acts/{act_id}", status_code=303)

@router.post("/transfer_acts/{act_id}/delete", name="transfer_acts_delete")
def transfer_acts_delete(act_id: int, db: Session = Depends(get_db)):
    act = db.query(TransferAct).get(act_id)
    if act:
        db.delete(act)
        db.commit()
    return RedirectResponse(url="/transfer_acts", status_code=303)

@router.get("/transfer_acts/{act_id}/pdf", name="transfer_act_pdf")
def transfer_act_pdf(act_id: int, db: Session = Depends(get_db)):
    act = db.query(TransferAct).get(act_id)
    if not act:
        raise HTTPException(status_code=404, detail="Акт передачи не найден")

    html_str = render_transfer_act_pdf_html(act)
    pdf_io = html_to_pdf(html_str)

    filename = f"transfer_act_{act_id}.pdf"
    headers = {
        "Content-Disposition": f"attachment; filename={filename}"
    }
    return StreamingResponse(pdf_io, media_type="application/pdf", headers=headers)