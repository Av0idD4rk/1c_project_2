# app/routers/owners.py

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.owner import Owner

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/owners", name="owners_list")
def owners_list(request: Request, db: Session = Depends(get_db)):
    owners = db.query(Owner).all()
    return templates.TemplateResponse("owners/list.html", {"request": request, "owners": owners})

@router.get("/owners/create", name="owners_create_form")
def owners_create_form(request: Request):
    return templates.TemplateResponse("owners/create.html", {"request": request})

@router.post("/owners/create", name="owners_create")
def owners_create(name: str = Form(...), db: Session = Depends(get_db)):
    new_owner = Owner(name=name)
    db.add(new_owner)
    db.commit()
    return RedirectResponse(url="/owners", status_code=303)

@router.get("/owners/{owner_id}", name="owners_detail")
def owners_detail(owner_id: int, request: Request, db: Session = Depends(get_db)):
    owner = db.query(Owner).get(owner_id)
    if not owner:
        return RedirectResponse(url="/owners", status_code=303)
    return templates.TemplateResponse("owners/detail.html", {"request": request, "owner": owner})

@router.get("/owners/{owner_id}/edit", name="owners_edit_form")
def owners_edit_form(owner_id: int, request: Request, db: Session = Depends(get_db)):
    owner = db.query(Owner).get(owner_id)
    if not owner:
        return RedirectResponse(url="/owners", status_code=303)
    return templates.TemplateResponse("owners/edit.html", {"request": request, "owner": owner})

@router.post("/owners/{owner_id}/edit", name="owners_edit")
def owners_edit(owner_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    owner = db.query(Owner).get(owner_id)
    if not owner:
        return RedirectResponse(url="/owners", status_code=303)
    owner.name = name
    db.commit()
    return RedirectResponse(url=f"/owners/{owner_id}", status_code=303)

@router.post("/owners/{owner_id}/delete", name="owners_delete")
def owners_delete(owner_id: int, db: Session = Depends(get_db)):
    owner = db.query(Owner).get(owner_id)
    if owner:
        db.delete(owner)
        db.commit()
    return RedirectResponse(url="/owners", status_code=303)
