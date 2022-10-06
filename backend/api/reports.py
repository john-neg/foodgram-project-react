import io

from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas


def cart_report(response):
    """Генерирует отчет - список ингредиентов для покупки."""

    buffer = io.BytesIO()
    canvas = Canvas(buffer, pagesize=A4)
    pdfmetrics.registerFont(TTFont("FreeSans", "data/FreeSans.ttf"))
    canvas.setFont("FreeSans", 18)
    canvas.drawString(220, 790, "Список покупок:")
    canvas.setFont("FreeSans", 14)
    start_pos = 750
    for count, ingredient in enumerate(response):
        canvas.drawString(
            50,
            start_pos,
            f"{count + 1}. {ingredient[0].capitalize()} - "
            f"{ingredient[2]} {ingredient[1]}",
        )
        start_pos -= 15
    canvas.showPage()
    canvas.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename="cart_report.pdf")
