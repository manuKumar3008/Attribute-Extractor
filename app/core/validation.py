import re
from datetime import datetime

def validate_output(data):
    errors = []
    parsed_dates = {}

    if data['firstname'] != "not mentioned" and not data['firstname'].isalpha():
        errors.append("First name must be alphabetic.")

    if data['lastname'] != "not mentioned" and not data['lastname'].isalpha():
        errors.append("Last name must be alphabetic.")

    if data['document_type'].lower() not in {"payslip", "invoice", "contract", "not mentioned"}:
        errors.append("Invalid document type.")

    # Validate and store dates safely
    for date_field in ["start_date", "end_date"]:
        if data[date_field] != "not mentioned":
            try:
                parsed_dates[date_field] = datetime.strptime(data[date_field].strip(), "%d-%m-%Y")
            except ValueError:
                errors.append(f"Invalid date format for {date_field}.")

    # Compare only if both dates were parsed correctly
    if "start_date" in parsed_dates and "end_date" in parsed_dates:
        if parsed_dates["start_date"] > parsed_dates["end_date"]:
            errors.append("Start date cannot be after end date.")

    

    # Amount validation
    try:
        if data['amount'] != "not mentioned":
            float(data['amount'])
    except:
        errors.append("Amount must be numeric.")

    # Currency validation
    if data['currency'] != "not mentioned" and not re.match(r"^[A-Z]{3}$", data['currency']):
        errors.append("Currency must be 3-letter ISO code.")

    # Document ID validation
    if data['document_id'] != "not mentioned" and not re.fullmatch(r"[a-zA-Z0-9]{6}", data['document_id']):
        errors.append("Document ID must be exactly 6 alphanumeric characters.")

    return errors
