from __future__ import annotations
import os
import json
import requests

SYSTEM = """You are DataLens AI, an enterprise data analyst. Use only the supplied computed facts. Never invent figures, rows, columns, causal relationships, or business facts. Clearly distinguish observation from hypothesis. If the evidence is insufficient, say so. Return concise executive-ready insights, then recommended next analytical checks."""


def ask_gemini(question: str, evidence: dict) -> str:
    key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is not configured")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    prompt = SYSTEM + "\n\nQuestion:\n" + question + "\n\nComputed evidence:\n" + json.dumps(evidence, default=str) + "\n\nRetrieved project context:\n" + json.dumps(evidence.get("retrieved_context", []), default=str)
    r = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=45)
    r.raise_for_status()
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]
