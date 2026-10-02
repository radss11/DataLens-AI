from __future__ import annotations
import io, sys
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from datalens_ai.data import load_dataset
from datalens_ai.agent import answer

app = FastAPI(title="DataLens AI API", version="1.0.0")

class Question(BaseModel):
    question: str

@app.get("/health")
def health():
    return {"status": "ok", "service": "datalens-ai"}

@app.post("/ask")
def ask(q: Question):
    if not q.question.strip():
        raise HTTPException(400, "Question cannot be empty")
    df = load_dataset()
    return answer(df, q.question)

@app.post("/ask-csv")
async def ask_csv(question: str, file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(400, "Only CSV files are supported")
    raw = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(raw))
    except Exception as exc:
        raise HTTPException(400, f"Invalid CSV: {exc}")
    return answer(df, question)
