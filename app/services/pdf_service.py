# app/pdf_service.py

import os
from io import BytesIO
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from app.models.order import Order
from app.models.arrival_act import ArrivalAct
from app.models.transfer_act import TransferAct
from app.models.return_act import ReturnAct

# Путь к папке с pdf-шаблонами
PDF_TEMPLATES_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",  # подняться на уровень выше
    "templates",
    "pdf"
)

# Инициализируем Jinja2 окружение
env = Environment(loader=FileSystemLoader(PDF_TEMPLATES_DIR))

def render_order_pdf_html(order: Order):
    """
    Генерирует HTML (str) для PDF Приказа.
    """
    template = env.get_template("order_pdf.html")
    # Экспонаты, связанные с приказом
    exhibits = order.exhibits  # SQLAlchemy relationship (M:N)

    # Подставляем данные в шаблон
    html_content = template.render(
        order=order,
        exhibits=exhibits
    )
    return html_content

def render_arrival_act_pdf_html(arrival_act: ArrivalAct):
    """
    Генерирует HTML (str) для PDF Акта поступления.
    """
    template = env.get_template("arrival_act_pdf.html")
    # Экспонаты в этом акте
    exhibits = arrival_act.exhibits

    # Подставляем данные в шаблон
    html_content = template.render(
        act=arrival_act,
        exhibits=exhibits
    )
    return html_content

def render_transfer_act_pdf_html(transfer_act: TransferAct):
    """
    Генерирует HTML (str) для PDF Акта передачи.
    """
    template = env.get_template("transfer_act_pdf.html")
    exhibits = transfer_act.exhibits

    html_content = template.render(
        act=transfer_act,
        exhibits=exhibits
    )
    return html_content

def render_return_act_pdf_html(return_act: ReturnAct):
    """
    Генерирует HTML (str) для PDF Акта возврата.
    """
    template = env.get_template("return_act_pdf.html")
    exhibits = return_act.exhibits

    html_content = template.render(
        act=return_act,
        exhibits=exhibits
    )
    return html_content

def html_to_pdf(html_content: str) -> BytesIO:
    """
    Конвертирует HTML-строку в PDF (BytesIO) с помощью WeasyPrint.
    """
    pdf_io = BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)
    return pdf_io
