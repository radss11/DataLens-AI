from __future__ import annotations
import os
from pathlib import Path
from .analysis import answer_locally
from .llm import ask_gemini
from .rag import LocalRAG

ROOT = Path(__file__).resolve().parents[2]
RAG = LocalRAG(ROOT / "docs" / "knowledge")

def answer(df, question: str) -> dict:
    evidence = answer_locally(df, question)
    evidence["retrieved_context"] = RAG.retrieve(question)
    provider = os.getenv("LLM_PROVIDER", "").lower()
    if provider == "gemini" and os.getenv("GEMINI_API_KEY"):
        try:
            evidence["llm_answer"] = ask_gemini(question, evidence)
            evidence["mode"] = "gemini-grounded-rag"
        except Exception as exc:
            evidence["llm_error"] = str(exc)
            evidence["llm_answer"] = "GenAI provider failed; showing deterministic evidence-based analysis instead."
    else:
        evidence["llm_answer"] = "\n".join(f"• {x}" for x in evidence["insights"])
    return evidence
