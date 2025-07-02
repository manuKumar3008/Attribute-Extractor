import dspy
import json
from dspy.signatures import Signature
from app.core.date_utils import infer_dates

class ExtractAttributes(Signature):
    query: str = dspy.InputField(desc="User query in natural language")
    context: str = dspy.InputField(desc="Previously extracted data as JSON")

    firstname: str = dspy.OutputField(desc="First name if explicitly mentioned")
    lastname: str = dspy.OutputField(desc="Last name if explicitly mentioned")
    document_type: str = dspy.OutputField(desc="Document type like payslip, invoice")
    time_expression: str = dspy.OutputField(desc="Time range or expression")
    amount: str = dspy.OutputField(desc="Amount if specified")
    currency: str = dspy.OutputField(desc="Currency if mentioned (e.g., USD)")
    document_id: str = dspy.OutputField(desc="Document ID if provided")

class AttributeExtractor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.program = dspy.Predict(ExtractAttributes)

    def forward(self, user_query, existing_data=None):
        context_json = json.dumps(existing_data or {})
        resp = self.program(query=user_query, context=context_json)

        time_expr = resp.time_expression.strip()
        start_date, end_date = infer_dates(time_expr, user_query)
        year = start_date[-4:] if start_date not in ("", "not mentioned") else ""

        result = {
            "firstname": resp.firstname.strip() or "not mentioned",
            "lastname": resp.lastname.strip() or "not mentioned",
            "document_type": resp.document_type.strip() or "not mentioned",
            "time_expression": time_expr or "not mentioned",
            "start_date": start_date,
            "end_date": end_date,
            "year": year,
            "amount": resp.amount.strip() or "not mentioned",
            "currency": resp.currency.strip() or "not mentioned",
            "document_id": resp.document_id.strip() or "not mentioned",
        }

        print("[DEBUG] Extracted fields:", result)
        return result