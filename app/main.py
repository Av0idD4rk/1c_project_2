# app/main.py

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.exhibition import Exhibition
from app.models.order import Order
from app.routers import owners, exhibits, exhibitions, orders, arrival_acts, transfer_acts, return_acts
from app.services.orders_service import calculate_stage

app = FastAPI(title="Exhibition Management")

# Указываем папку с шаблонами (если не сделано ранее)
templates = Jinja2Templates(directory="app/templates")

# Если нужен доступ к статике (CSS, JS), монтируем папку:
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Подключаем роутеры (как делали раньше)
app.include_router(owners.router)
app.include_router(exhibits.router)
app.include_router(exhibitions.router)
app.include_router(orders.router)
app.include_router(arrival_acts.router)
app.include_router(transfer_acts.router)
app.include_router(return_acts.router)

from fastapi import Request

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@app.get("/")
def read_index(request: Request, db: Session = Depends(get_db)):
    exhibitions = db.query(Exhibition).all()

    # Создаём список «(выставка, стадия)»
    exhibitions_with_stage = []
    for ex in exhibitions:
        try:
            order = db.query(Order).filter_by(exhibition_id=ex.id).first()
            stage = calculate_stage(order, db)
        except AttributeError:
            stage='Запланировано'

        exhibitions_with_stage.append({"exhibition": ex, "stage": stage})

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "exhibitions_with_stage": exhibitions_with_stage
        }
    )
# >>> Настраиваем обработчик <<<
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Ловим любые HTTPException и вместо JSON отдаём HTML-страницу error.html
    """
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "status_code": exc.status_code,
            "detail": exc.detail
        },
        status_code=exc.status_code
    )