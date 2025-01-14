
import os
from io import BytesIO
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML

from app.models.order import Order
from app.models.arrival_act import ArrivalAct
from app.models.transfer_act import TransferAct
from app.models.return_act import ReturnAct

PDF_TEMPLATES_DIR = os.path.join(
    os.path.dirname(__file__),
    "..",
    "templates",
    "pdf"
)

env = Environment(loader=FileSystemLoader(PDF_TEMPLATES_DIR))

def render_order_pdf_html(order: Order):
    template = env.get_template("order_pdf.html")
    exhibits = order.exhibits

    html_content = template.render(
        order=order,
        exhibits=exhibits
    )
    return html_content

def render_arrival_act_pdf_html(arrival_act: ArrivalAct):
    template = env.get_template("arrival_act_pdf.html")
    exhibits = arrival_act.exhibits

    html_content = template.render(
        act=arrival_act,
        exhibits=exhibits
    )
    return html_content

def render_transfer_act_pdf_html(transfer_act: TransferAct):
    template = env.get_template("transfer_act_pdf.html")
    exhibits = transfer_act.exhibits

    html_content = template.render(
        act=transfer_act,
        exhibits=exhibits
    )
    return html_content

def render_return_act_pdf_html(return_act: ReturnAct):
    template = env.get_template("return_act_pdf.html")
    exhibits = return_act.exhibits

    html_content = template.render(
        act=return_act,
        exhibits=exhibits
    )
    return html_content

def html_to_pdf(html_content: str) -> BytesIO:
    pdf_io = BytesIO()
    HTML(string=html_content).write_pdf(pdf_io)
    pdf_io.seek(0)
    return pdf_io
