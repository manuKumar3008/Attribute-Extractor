import dspy
import json
from app.core.signatures import FollowUpSignature

class FollowUpGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.program = dspy.Predict(FollowUpSignature)

    def forward(self, extracted_data, missing_fields):
        if not isinstance(extracted_data, str):
            extracted_data = json.dumps(extracted_data)
        if isinstance(missing_fields, list):
            missing_fields = ", ".join(missing_fields)

        print("[DEBUG] Missing fields:", missing_fields)
        try:
            response = self.program(
                extracted_data=extracted_data,
                missing_fields=missing_fields
            )
            print("[DEBUG] Follow-up response:", response)
        except Exception as e:
            print("[ERROR] FollowUp prediction failed:", e)
            response = type("Fallback", (), {"next_question": ""})()

        fallback = f"Could you please provide your {missing_fields.split(',')[0].strip()}?"
        question = getattr(response, "next_question", "").strip()
        response.next_question = question or fallback

        return response