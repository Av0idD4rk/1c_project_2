# app/services/orders_service.py  (пример отдельного слоя)

from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.arrival_act import ArrivalAct
from app.models.transfer_act import TransferAct
from app.models.return_act import ReturnAct
from datetime import date

def calculate_stage(order: Order, db: Session) -> str:
    """
    Возвращает строку, описывающую стадию выставки,
    исходя из существующих Arrival/Transfer/Return актов и дат.
    """
    # Если даты (в т.ч. текущее состояние) могут влиять, берём order.start_date / end_date
    today = date.today()

    # 1) Нет ArrivalAct => "PLANNED"
    arrival_count = db.query(ArrivalAct).filter_by(order_id=order.id).count()
    if arrival_count == 0:
        return "Запланировано"

    # 2) Есть хотя бы один ArrivalAct, но ни одного Transfer => "ARRIVED_BUT_NOT_TRANSFERRED"
    transfer_count = db.query(TransferAct).filter_by(order_id=order.id).count()
    if transfer_count == 0:
        return "Прибытие экспонатов"

    # 3) Есть Transfer, но нет Return => "IN_PROGRESS"
    return_count = db.query(ReturnAct).filter_by(order_id=order.id).count()
    if return_count == 0:
        # Проверим, закончилась ли выставка по датам?
        if today > order.end_date:
            # Уже дата прошла, но ReturnAct всё ещё нет — можно назвать "WAITING_FOR_RETURN"
            return "Ожидаем возврата"
        else:
            # Выставка идёт
            return "Выставка идёт"

    # 4) Есть ReturnAct => "FINISHED"
    # Можно усложнить: если не все экспонаты вернулись, то стадия "PARTIAL_RETURN" и т.д.
    return "Выставка закончилась"

