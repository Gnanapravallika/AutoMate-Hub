
from fastapi import FastAPI, Request, UploadFile, File, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.config import settings
from app.services.csv_service import validate_csv
from app.services.pdf_service import generate_invoice
from app.services.email_service import send_email
import os

app = FastAPI(title=settings.PROJECT_NAME)

# Create temp directories if they don't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.INVOICE_DIR, exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/invoices", StaticFiles(directory=settings.INVOICE_DIR), name="invoices")

# Templates
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def process_csv(file: UploadFile = File(...)):
    contents = await file.read()
    
    # Validation
    validation_result = validate_csv(contents)
    if "error" in validation_result:
        return {"status": "error", "message": validation_result["error"]}
    
    if not validation_result["valid_rows"]:
         return {"status": "error", "message": "No valid rows found to process.", "details": validation_result}

    processed_count = 0
    email_success_count = 0
    errors = validation_result["errors"]
    generated_invoices = []
    
    for row in validation_result["valid_rows"]:
        try:
            # Generate Invoice
            pdf_path = generate_invoice(row)
            
            # Store for Response
            filename = os.path.basename(pdf_path)
            generated_invoices.append({
                "client": row.get("Client Name", "Client"),
                "url": f"/invoices/{filename}"
            })
            
            # Send Email
            subject = f"Invoice from {settings.PROJECT_NAME}"
            body = f"Dear {row.get('Client Name')},\n\nPlease find attached your invoice.\n\nThank you,\n{settings.PROJECT_NAME}"
            
            sent = send_email(
                to_email=row.get("Client Email"), 
                subject=subject, 
                body=body, 
                attachment_path=pdf_path
            )
            
            if sent:
                email_success_count += 1
            else:
                errors.append({"row": "N/A", "errors": [f"Failed to send email to {row.get('Client Email')}"]})
            
            processed_count += 1
            
        except Exception as e:
            errors.append({"row": "N/A", "errors": [f"Processing error: {str(e)}"]})

    return {
        "status": "success",
        "processed": processed_count,
        "email_sent": email_success_count,
        "errors": errors,
        "total_rows": validation_result["total_rows"],
        "generated_invoices": generated_invoices
    }
