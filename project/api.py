from fastapi import FastAPI
from pydantic import BaseModel
from llm_engine import generate_interview_questions

app = FastAPI()

class JobInput(BaseModel):
    job_description: str

@app.get("/")
def home():
    return {"message": "AI Interview Kit Generator API running"}

@app.post("/generate")
def generate_questions(data: JobInput):
    try:
        result = generate_interview_questions(data.job_description)
        return result
    except Exception as e:
        return {"error": str(e)}