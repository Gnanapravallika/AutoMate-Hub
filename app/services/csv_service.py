import pandas as pd
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
import io

REQUIRED_COLUMNS = ["Client Name", "Client Email", "Invoice Amount", "Due Date"]

def validate_csv(file_content: bytes) -> dict:
    """
    Validates the CSV file content.
    Returns a dict with 'valid_rows', 'errors', and 'total_rows'.
    """
    try:
        df = pd.read_csv(io.BytesIO(file_content))
    except Exception as e:
        return {"error": f"Invalid CSV file: {str(e)}"}

    # Check for empty file
    if df.empty:
        return {"error": "CSV file is empty"}

    # Check for missing columns
    missing_columns = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_columns:
        return {"error": f"Missing required columns: {', '.join(missing_columns)}"}

    valid_rows = []
    errors = []
    
    # Normalize column names (strip whitespace)
    df.columns = df.columns.str.strip()

    for index, row in df.iterrows():
        row_num = index + 2  # 1-indexed, +1 for header
        row_data = row.to_dict()
        row_errors = []

        # Validate Client Name
        if pd.isna(row.get("Client Name")) or str(row.get("Client Name")).strip() == "":
            row_errors.append("Missing Client Name")

        # Validate Email
        email = row.get("Client Email")
        if pd.isna(email):
            row_errors.append("Missing Client Email")
        else:
            try:
                validate_email(str(email).strip(), check_deliverability=False)
                row_data["Client Email"] = str(email).strip()
            except EmailNotValidError:
                row_errors.append("Invalid Client Email format")

        # Validate Amount
        amount = row.get("Invoice Amount")
        if pd.isna(amount):
            row_errors.append("Missing Invoice Amount")
        else:
            try:
                val = float(str(amount).replace(",", "").strip()) # Handle "1,000.00"
                row_data["Invoice Amount"] = val
            except ValueError:
                row_errors.append("Invoice Amount must be numeric")

        # Validate Due Date
        due_date = row.get("Due Date")
        if pd.isna(due_date):
            row_errors.append("Missing Due Date")
        else:
            # Try parsing a few common formats
            date_str = str(due_date).strip()
            parsed_date = None
            for fmt in ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"]:
                try:
                    parsed_date = datetime.strptime(date_str, fmt).date()
                    break
                except ValueError:
                    continue
            
            if parsed_date:
                row_data["Due Date"] = parsed_date
            else:
                row_errors.append(f"Invalid Date format (use YYYY-MM-DD): {date_str}")

        if row_errors:
            errors.append({"row": row_num, "errors": row_errors, "data": row_data})
        else:
            valid_rows.append(row_data)

    return {
        "valid_rows": valid_rows,
        "errors": errors,
        "total_rows": len(df)
    }
