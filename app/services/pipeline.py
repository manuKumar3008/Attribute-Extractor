from app.core.extractor import AttributeExtractor
from app.core.validation_dspy import DSPyValidationModule
from app.core.followups import FollowUpGenerator

# Define what "missing" means more clearly
def is_missing(value):
    val = str(value).strip().lower()
    return (
        val in {"", "none", "not mentioned", None}
        or "not mentioned in the query" in val
        or (val.startswith("{") and val.endswith("}"))
    )

def run_query(user_query, existing_data=None, field_being_asked=None):
    extractor = AttributeExtractor()
    result = extractor.forward(user_query, existing_data)

    validator = DSPyValidationModule()
    errors = validator.forward(result)

    # Enhanced missing detection
    cleaned = [e for e in errors if is_missing(result.get(e, ""))]

    follow_ups, next_field = [], None
    if cleaned:
        next_field = cleaned[0]
        follow = FollowUpGenerator().forward(result, cleaned)
        question = getattr(follow, "next_question", "").strip()
        follow_ups = [question] if question else [f"What is your {next_field}?"]

    return result, cleaned, follow_ups, next_field, None