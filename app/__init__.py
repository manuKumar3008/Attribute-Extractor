import dspy

lm = dspy.LM(
    model='mistral-small',
    api_key='UG7bneOB0yghP9ZYDG4ZPlrDsBmfiSGc',
    api_base='https://api.mistral.ai/v1',
    provider='mistralai',
)

dspy.configure(lm=lm)

