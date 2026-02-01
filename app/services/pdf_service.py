from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
import os
import uuid
from datetime import datetime
from app.core.config import settings

def generate_invoice(data: dict) -> str:
    """
    Generates a PDF invoice for the given data.
    Returns the absolute path to the generated PDF.
    """
    invoice_id = str(uuid.uuid4())[:8].upper()
    filename = f"invoice_{invoice_id}.pdf"
    filepath = os.path.join(settings.INVOICE_DIR, filename)

    c = canvas.Canvas(filepath, pagesize=letter)
    width, height = letter

    # --- Header ---
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor("#3182ce"))
    c.drawString(1 * inch, height - 1 * inch, "INVOICE")

    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawString(1 * inch, height - 1.3 * inch, f"Invoice #: {invoice_id}")
    c.drawString(1 * inch, height - 1.5 * inch, f"Date: {datetime.now().strftime('%Y-%m-%d')}")

    # --- Sender Details (Placeholder) ---
    c.drawRightString(width - 1 * inch, height - 1 * inch, "AutoMate Hub")
    c.drawRightString(width - 1 * inch, height - 1.2 * inch, "automator@example.com")

    # --- Separator ---
    c.setStrokeColor(colors.lightgrey)
    c.line(1 * inch, height - 1.7 * inch, width - 1 * inch, height - 1.7 * inch)

    # --- Bill To ---
    y_position = height - 2.5 * inch
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1 * inch, y_position, "Bill To:")
    c.setFont("Helvetica", 12)
    c.drawString(1 * inch, y_position - 0.25 * inch, data.get("Client Name", "Valued Client"))
    c.drawString(1 * inch, y_position - 0.45 * inch, data.get("Client Email", ""))

    # --- Invoice Table ---
    y_position -= 1.5 * inch
    c.setFillColor(colors.HexColor("#edf2f7"))
    c.rect(1 * inch, y_position, width - 2 * inch, 0.4 * inch, fill=1, stroke=0)
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(1.2 * inch, y_position + 0.15 * inch, "DESCRIPTION")
    c.drawString(4 * inch, y_position + 0.15 * inch, "DUE DATE")
    c.drawRightString(width - 1.2 * inch, y_position + 0.15 * inch, "AMOUNT")

    # Row 1
    y_position -= 0.4 * inch
    c.setFont("Helvetica", 10)
    c.drawString(1.2 * inch, y_position + 0.15 * inch, "Professional Services")
    
    due_date = data.get("Due Date")
    if isinstance(due_date, str):
        due_date_str = due_date
    else:
        due_date_str = due_date.strftime("%Y-%m-%d") if due_date else ""
        
    c.drawString(4 * inch, y_position + 0.15 * inch, due_date_str)
    
    amount = data.get("Invoice Amount", 0)
    c.drawRightString(width - 1.2 * inch, y_position + 0.15 * inch, f"${amount:,.2f}")

    # Line
    c.setStrokeColor(colors.lightgrey)
    c.line(1 * inch, y_position, width - 1 * inch, y_position)

    # --- Total ---
    y_position -= 0.5 * inch
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(width - 1.2 * inch, y_position, f"Total: ${amount:,.2f}")

    c.save()
    return filepath
