from fastapi import FastAPI
from pydantic import BaseModel
from app.services.pipeline import run_query

app = FastAPI()

class QueryInput(BaseModel):
    query: str

@app.post("/extract/")
def extract_attributes(input: QueryInput):
    return run_query(input.query)
