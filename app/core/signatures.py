from dspy import Signature, InputField, OutputField

class ValidateFieldsSignature(Signature):
    extracted_fields: str = InputField(desc="Extracted document fields in JSON format.")
    validation_errors: str = OutputField(desc="List of validation errors or missing fields.")

class FollowUpSignature(Signature):
    extracted_data: str = InputField(desc="Extracted data as JSON")
    missing_fields: str = InputField(desc="Field(s) missing or invalid")
    next_question: str = OutputField(desc="A natural language question asking for the missing field.")