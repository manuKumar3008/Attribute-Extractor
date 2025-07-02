import dspy
import json
from app.core.signatures import ValidateFieldsSignature

# Fields we expect to be extracted
EXPECTED_FIELDS = [
    "firstname", "lastname", "document_type", "time_expression",
    "start_date", "end_date", "year", "amount", "currency", "document_id"
]

# Smart checker for missing or placeholder values
def is_missing(value):
    val = str(value).strip().lower()
    return (
        val in {"", "none", "not mentioned", None}
        or "not mentioned in the query" in val
        or val.startswith("{") and val.endswith("}")
    )

class DSPyValidationModule(dspy.Module):
    def __init__(self):
        super().__init__()
        self.program = dspy.Predict(ValidateFieldsSignature)

    def forward(self, extracted_data):
        try:
            if not isinstance(extracted_data, str):
                extracted_data = json.dumps(extracted_data)

            # Attempt LLM-based validation
            response = self.program(extracted_fields=extracted_data)
            raw = getattr(response, "validation_errors", "")
            parsed = json.loads(raw) if raw.strip().startswith("[") else []

            if parsed:
                print("[DEBUG] DSPy returned validation errors:", parsed)
                return parsed

            # If DSPy returns nothing, fallback to manual
            print("[DEBUG] DSPy returned no errors, applying fallback validation.")
            data = json.loads(extracted_data)
            return [field for field in EXPECTED_FIELDS if is_missing(data.get(field))]

        except Exception as e:
            print("[ERROR] DSPy validation failed, applying fallback:", e)
            try:
                data = json.loads(extracted_data)
                return [field for field in EXPECTED_FIELDS if is_missing(data.get(field))]
            except Exception as e2:
                print("[FATAL] Fallback validation also failed:", e2)
                return []