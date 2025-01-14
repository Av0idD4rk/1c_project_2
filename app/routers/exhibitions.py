from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.arrival_act import ArrivalAct
from app.models.exhibition import Exhibition
from app.models.order import Order
from app.models.return_act import ReturnAct
from app.models.transfer_act import TransferAct

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/exhibitions", name="exhibitions_list")
def exhibitions_list(request: Request, db: Session = Depends(get_db)):
    exhibitions = db.query(Exhibition).all()
    return templates.TemplateResponse("exhibitions/list.html", {"request": request, "exhibitions": exhibitions})

@router.get("/exhibitions/create", name="exhibitions_create_form")
def exhibitions_create_form(request: Request):
    return templates.TemplateResponse("exhibitions/create.html", {"request": request})

@router.post("/exhibitions/create", name="exhibitions_create")
def exhibitions_create(
    title: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    exhibition = Exhibition(title=title, description=description)
    db.add(exhibition)
    db.commit()
    return RedirectResponse(url="/exhibitions", status_code=303)


@router.get("/exhibitions/{exhibition_id}")
def exhibitions_detail(exhibition_id: int, request: Request, db: Session = Depends(get_db)):
    exhibition = db.query(Exhibition).get(exhibition_id)
    if not exhibition:
        return RedirectResponse(url="/exhibitions", status_code=303)

    order = db.query(Order).filter(Order.exhibition_id == exhibition.id).first()
    print(order)
    exhibits = []
    arrival_acts = []
    transfer_acts = []
    return_acts = []

    if order:
        exhibits = order.exhibits  # SQLAlchemy relationship

        arrival_acts = db.query(ArrivalAct).filter(ArrivalAct.order_id == order.id).all()
        transfer_acts = db.query(TransferAct).filter(TransferAct.order_id == order.id).all()
        return_acts = db.query(ReturnAct).filter(ReturnAct.order_id == order.id).all()

    return templates.TemplateResponse("exhibitions/detail.html", {
        "request": request,
        "exhibition": exhibition,
        "order": order,
        "exhibits": exhibits,
        "arrival_acts": arrival_acts,
        "transfer_acts": transfer_acts,
        "return_acts": return_acts
    })
@router.get("/exhibitions/{exhibition_id}/edit", name="exhibitions_edit_form")
def exhibitions_edit_form(exhibition_id: int, request: Request, db: Session = Depends(get_db)):
    exhibition = db.query(Exhibition).get(exhibition_id)
    if not exhibition:
        return RedirectResponse(url="/exhibitions", status_code=303)
    return templates.TemplateResponse("exhibitions/edit.html", {"request": request, "exhibition": exhibition})

@router.post("/exhibitions/{exhibition_id}/edit", name="exhibitions_edit")
def exhibitions_edit(
    exhibition_id: int,
    title: str = Form(...),
    description: str = Form(None),
    db: Session = Depends(get_db)
):
    exhibition = db.query(Exhibition).get(exhibition_id)
    if not exhibition:
        return RedirectResponse(url="/exhibitions", status_code=303)
    exhibition.title = title
    exhibition.description = description
    db.commit()
    return RedirectResponse(url=f"/exhibitions/{exhibition_id}", status_code=303)

@router.post("/exhibitions/{exhibition_id}/delete", name="exhibitions_delete")
def exhibitions_delete(exhibition_id: int, db: Session = Depends(get_db)):
    exhibition = db.query(Exhibition).get(exhibition_id)
    if exhibition:
        db.delete(exhibition)
        db.commit()
    return RedirectResponse(url="/exhibitions", status_code=303)
