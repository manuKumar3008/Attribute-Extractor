import re
from datetime import datetime

def validate_output(data):
    errors = []
    parsed_dates = {}

    # --- First Name ---
    if not data.get("firstname") or data["firstname"] == "not mentioned":
        errors.append("First name is missing.")
    elif not data["firstname"].isalpha():
        errors.append("First name must be alphabetic.")

    # --- Last Name ---
    if not data.get("lastname") or data["lastname"] == "not mentioned":
        errors.append("Last name is missing.")
    elif not data["lastname"].isalpha():
        errors.append("Last name must be alphabetic.")

    # --- Document Type ---
    if not data.get("document_type") or data["document_type"] == "not mentioned":
        errors.append("Document type is missing.")
    elif data["document_type"].lower() not in {"payslip", "invoice", "contract", "not mentioned"}:
        errors.append("Invalid document type.")

    # --- Dates ---
    for date_field in ["start_date", "end_date"]:
        if not data.get(date_field) or data[date_field] == "not mentioned":
            errors.append(f"{date_field.replace('_', ' ').capitalize()} is missing.")
        else:
            try:
                parsed_dates[date_field] = datetime.strptime(data[date_field].strip(), "%d-%m-%Y")
            except ValueError:
                errors.append(f"Invalid date format for {date_field}.")

    # Compare start/end dates if both are valid
    if "start_date" in parsed_dates and "end_date" in parsed_dates:
        if parsed_dates["start_date"] > parsed_dates["end_date"]:
            errors.append("Start date cannot be after end date.")

    # --- Year ---
    if not data.get("year") or data["year"] == "not mentioned":
        errors.append("Year is missing.")

    # --- Amount ---
    if not data.get("amount") or data["amount"] == "not mentioned":
        errors.append("Amount is missing.")
    else:
        try:
            float(data["amount"])
        except:
            errors.append("Amount must be numeric.")

    # --- Currency ---
    if not data.get("currency") or data["currency"] == "not mentioned":
        errors.append("Currency is missing.")
    elif not re.match(r"^[A-Z]{3}$", data["currency"]):
        errors.append("Currency must be 3-letter ISO code.")

    # --- Document ID ---
    if not data.get("document_id") or data["document_id"] == "not mentioned":
        errors.append("Document ID is missing.")
    elif not re.fullmatch(r"[a-zA-Z0-9]{6}", data["document_id"]):
        errors.append("Document ID must be exactly 6 alphanumeric characters.")

    return errors
