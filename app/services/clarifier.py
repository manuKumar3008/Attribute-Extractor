# app/services/clarifier.py

import dspy

class ClarifySignature(dspy.Signature):
    """Generate follow-up questions for missing or invalid fields."""
    context = dspy.InputField()
    missing = dspy.InputField()
    follow_ups = dspy.OutputField()

class Clarifier(dspy.Module):
    def __init__(self, missing):
        super().__init__()
        self.missing = missing
        self.generator = dspy.Predict(ClarifySignature)

    def forward(self, context):
        response = self.generator(
            context=context,
            missing=", ".join(self.missing)
        )
        return response.follow_ups.split("\n")
