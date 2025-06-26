import dspy
from dspy.signatures import Signature

# Signature defining I/O fields
class GenerateSingleFollowUp(Signature):
    extracted_data: str = dspy.InputField(desc="Current document fields extracted from user input.")
    missing_fields: str = dspy.InputField(desc="Fields that are missing or invalid.")
    next_question: str = dspy.OutputField(desc="Ask one specific, contextual question to fill one missing field.")


# DSPy module using Chain-of-Thought with prompt
class FollowUpGenerator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.program = dspy.ChainOfThought(
            GenerateSingleFollowUp,
            prompt=(
                "You are a smart assistant that helps complete missing information for document extraction.\n"
                "Use the extracted fields and missing field names to choose the most important next field to ask about.\n"
                "Ask exactly one clear, user-friendly follow-up question to gather it.\n\n"
                "Example:\n"
                "Extracted: {\"firstname\": \"John\", \"lastname\": \"not mentioned\"}\n"
                "Missing: lastname\n"
                "Question: 🧑 What is the last name?\n\n"
                "Now respond for the following:\n"
                "Extracted: {extracted_data}\n"
                "Missing: {missing_fields}\n"
                "Question:"
            )
        )

    def forward(self, extracted_data, missing_fields):
        return self.program(
            extracted_data=extracted_data,
            missing_fields=missing_fields
        )
