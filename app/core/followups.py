import dspy
from dspy.signatures import Signature

class GenerateSingleFollowUp(Signature):
    extracted_data: str = dspy.InputField(desc="Current document fields extracted from user input.")
    missing_fields: str = dspy.InputField(desc="Fields that are missing or invalid.")
    next_question: str = dspy.OutputField(desc="Ask one specific, contextual question to fill one missing field.")

class FollowUpGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.program = dspy.ChainOfThought(GenerateSingleFollowUp)

    def forward(self, extracted_data, missing_fields):
        return self.program(
            extracted_data=extracted_data,
            missing_fields=missing_fields
        )
