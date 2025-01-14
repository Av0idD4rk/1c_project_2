import datetime
from app.database import SessionLocal
from app.models.owner import Owner
from app.models.exhibit import Exhibit
from app.models.exhibition import Exhibition
from app.models.order import Order
from app.models.arrival_act import ArrivalAct
from app.models.transfer_act import TransferAct
from app.models.return_act import ReturnAct


def seed_data():
    db = SessionLocal()

    existing_exhibitions = db.query(Exhibition).count()
    if existing_exhibitions > 0:
        print("Данные уже существуют, пропускаем заполнение.")
        db.close()
        return

    owner1 = Owner(name="ООО 'Наука и Культура'")
    owner2 = Owner(name="Музей Искусств")
    db.add_all([owner1, owner2])
    db.commit()

    ex1 = Exhibit(name="Картина 'Золотая осень'", owner_id=owner1.id)
    ex2 = Exhibit(name="Скульптура 'Мыслитель'", owner_id=owner1.id)
    ex3 = Exhibit(name="Картина 'Пейзаж с соснами'", owner_id=owner2.id)
    ex4 = Exhibit(name="Редкий артефакт 'Вазопись'", owner_id=owner2.id)
    db.add_all([ex1, ex2, ex3, ex4])
    db.commit()

    exh1 = Exhibition(title="Выставка Современного Искусства", description="Современное искусство 20-21 века")
    exh2 = Exhibition(title="Историческая Выставка", description="Артефакты и реликвии из прошлого")
    db.add_all([exh1, exh2])
    db.commit()

    order1 = Order(
        exhibition_id=exh1.id,
        created_at=datetime.datetime.now(),
        start_date=datetime.date(2023, 9, 1),
        end_date=datetime.date(2023, 9, 30),
        venue="Главный зал",
    )
    order1.exhibits = [ex1, ex2]

    order2 = Order(
        exhibition_id=exh2.id,
        created_at=datetime.datetime.now(),
        start_date=datetime.date(2023, 10, 1),
        end_date=datetime.date(2023, 10, 15),
        venue="Второй павильон",
    )
    order2.exhibits = [ex3, ex4]

    db.add_all([order1, order2])
    db.commit()

    arrival1 = ArrivalAct(order_id=order1.id)
    arrival1.exhibits = [ex1, ex2]
    arrival2 = ArrivalAct(order_id=order2.id)
    arrival2.exhibits = [ex3, ex4]
    db.add_all([arrival1, arrival2])
    db.commit()

    transfer1 = TransferAct(order_id=order1.id)
    transfer1.exhibits = [ex1, ex2]
    transfer2 = TransferAct(order_id=order2.id)
    transfer2.exhibits = [ex3, ex4]
    db.add_all([transfer1, transfer2])
    db.commit()

    return1 = ReturnAct(order_id=order1.id)
    return1.exhibits = [ex1, ex2]
    return2 = ReturnAct(order_id=order2.id)
    return2.exhibits = [ex3, ex4]
    db.add_all([return1, return2])
    db.commit()

    db.close()
    print("Тестовые данные успешно добавлены.")


if __name__ == "__main__":
    seed_data()