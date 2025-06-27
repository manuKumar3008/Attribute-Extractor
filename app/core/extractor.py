import dspy
from dspy.signatures import Signature

class ExtractAttributes(Signature):
    query: str = dspy.InputField(desc="User query in natural language")

    firstname: str = dspy.OutputField(desc="First name if explicitly mentioned, otherwise leave blank")
    lastname: str = dspy.OutputField(desc="Last name if explicitly mentioned, otherwise leave blank")
    document_type: str = dspy.OutputField(desc="Document type like invoice, payslip, etc.")
    time_expression: str = dspy.OutputField(desc="Time range or expression, like 'last 3 months'")
    amount: str = dspy.OutputField(desc="Amount if specified, else leave blank")
    currency: str = dspy.OutputField(desc="Currency if mentioned, else leave blank")
    document_id: str = dspy.OutputField(desc="6-character ID if provided, else leave blank")


class AttributeExtractor(dspy.Module):
    def __init__(self):
        super().__init__()
        self.program = dspy.Predict(ExtractAttributes)

    def forward(self, query):
        return self.program(query=query) 