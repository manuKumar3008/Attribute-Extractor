from app.core.extractor import AttributeExtractor
from app.core.date_utils import infer_dates
from app.core.validation import validate_output
from app.core.followups import FollowUpGenerator
from datetime import datetime
import json

def normalize(value):
    if value is None or str(value).strip().lower() in [
        "", "not mentioned", "not provided in the query.", "not specified in the query."
    ]:
        return "not mentioned"
    return str(value).strip()

def run_query(user_query, existing_data=None, field_being_asked=None):
    extractor = AttributeExtractor()

    try:
        raw_output = extractor.forward(query=user_query)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to get valid response from LM: {e}")

    extracted = {
        "firstname": normalize(getattr(raw_output, "firstname", None)),
        "lastname": normalize(getattr(raw_output, "lastname", None)),
        "document_type": normalize(getattr(raw_output, "document_type", None)),
        "amount": normalize(getattr(raw_output, "amount", None)),
        "currency": normalize(getattr(raw_output, "currency", None)),
        "document_id": normalize(getattr(raw_output, "document_id", None)),
        "time_expression": getattr(raw_output, "time_expression", None),
    }

    if existing_data:
        for key, value in existing_data.items():
            if value != "not mentioned" and extracted.get(key) == "not mentioned":
                extracted[key] = value

    if field_being_asked:
        extracted[field_being_asked] = normalize(user_query)

    start_date, end_date = infer_dates(extracted.get("time_expression"), user_query)
    if existing_data:
        if existing_data.get("start_date") != "not mentioned" and start_date == "not mentioned":
            start_date = existing_data["start_date"]
        if existing_data.get("end_date") != "not mentioned" and end_date == "not mentioned":
            end_date = existing_data["end_date"]

    try:
        year = datetime.strptime(end_date, "%d-%m-%Y").year if end_date != "not mentioned" else "not mentioned"
    except Exception:
        year = "not mentioned"

    result = {
        "firstname": extracted["firstname"],
        "lastname": extracted["lastname"],
        "document_type": extracted["document_type"],
        "start_date": start_date,
        "end_date": end_date,
        "year": str(year),
        "amount": extracted["amount"],
        "currency": extracted["currency"],
        "document_id": extracted["document_id"],
    }

    errors = validate_output(result)

    follow_ups = []
    next_field_to_ask = None
    if errors:
        followup_model = FollowUpGenerator()
        next_field_to_ask = errors[0]
        followup_output = followup_model.forward(
            extracted_data=json.dumps(result),
            missing_fields=next_field_to_ask
        )
        if followup_output.next_question:
            follow_ups.append(followup_output.next_question)

    return result, errors, follow_ups, next_field_to_ask
