
from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.arrival_act import ArrivalAct
from app.models.transfer_act import TransferAct
from app.models.return_act import ReturnAct
from datetime import date

def calculate_stage(order: Order, db: Session) -> str:
    today = date.today()

    arrival_count = db.query(ArrivalAct).filter_by(order_id=order.id).count()
    if arrival_count == 0:
        return "Запланировано"

    transfer_count = db.query(TransferAct).filter_by(order_id=order.id).count()
    if transfer_count == 0:
        return "Прибытие экспонатов"

    return_count = db.query(ReturnAct).filter_by(order_id=order.id).count()
    if return_count == 0:
        if today > order.end_date:
            return "Ожидаем возврата"
        else:
            # Выставка идёт
            return "Выставка идёт"

    return "Выставка закончилась"

