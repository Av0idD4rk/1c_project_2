# app/routers/exhibits.py

from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.exhibit import Exhibit
from app.models.owner import Owner

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/exhibits", name="exhibits_list")
def exhibits_list(request: Request, db: Session = Depends(get_db)):
    exhibits = db.query(Exhibit).all()
    return templates.TemplateResponse("exhibits/list.html", {"request": request, "exhibits": exhibits})

@router.get("/exhibits/create", name="exhibits_create_form")
def exhibits_create_form(request: Request, db: Session = Depends(get_db)):
    owners = db.query(Owner).all()
    return templates.TemplateResponse("exhibits/create.html", {"request": request, "owners": owners})

@router.post("/exhibits/create", name="exhibits_create")
def exhibits_create(name: str = Form(...), owner_id: int = Form(...), db: Session = Depends(get_db)):
    exhibit = Exhibit(name=name, owner_id=owner_id)
    db.add(exhibit)
    db.commit()
    return RedirectResponse(url="/exhibits", status_code=303)

@router.get("/exhibits/{exhibit_id}", name="exhibits_detail")
def exhibits_detail(exhibit_id: int, request: Request, db: Session = Depends(get_db)):
    exhibit = db.query(Exhibit).get(exhibit_id)
    if not exhibit:
        return RedirectResponse(url="/exhibits", status_code=303)
    return templates.TemplateResponse("exhibits/detail.html", {"request": request, "exhibit": exhibit})

@router.get("/exhibits/{exhibit_id}/edit", name="exhibits_edit_form")
def exhibits_edit_form(exhibit_id: int, request: Request, db: Session = Depends(get_db)):
    exhibit = db.query(Exhibit).get(exhibit_id)
    if not exhibit:
        return RedirectResponse(url="/exhibits", status_code=303)
    owners = db.query(Owner).all()
    return templates.TemplateResponse("exhibits/edit.html", {"request": request, "exhibit": exhibit, "owners": owners})

@router.post("/exhibits/{exhibit_id}/edit", name="exhibits_edit")
def exhibits_edit(exhibit_id: int, name: str = Form(...), owner_id: int = Form(...), db: Session = Depends(get_db)):
    exhibit = db.query(Exhibit).get(exhibit_id)
    if not exhibit:
        return RedirectResponse(url="/exhibits", status_code=303)
    exhibit.name = name
    exhibit.owner_id = owner_id
    db.commit()
    return RedirectResponse(url=f"/exhibits/{exhibit_id}", status_code=303)

@router.post("/exhibits/{exhibit_id}/delete", name="exhibits_delete")
def exhibits_delete(exhibit_id: int, db: Session = Depends(get_db)):
    exhibit = db.query(Exhibit).get(exhibit_id)
    if exhibit:
        db.delete(exhibit)
        db.commit()
    return RedirectResponse(url="/exhibits", status_code=303)
