# Interview guide

## 60-second explanation

DataLens AI is a GenAI-powered analytics assistant. A user can upload a structured dataset and ask a natural-language question. The system first computes evidence using Python and Pandas—profiling the data, calculating trends and group comparisons, and producing structured facts. Only those computed facts are passed to the LLM, which converts them into an executive-friendly explanation. This architecture deliberately separates computation from language generation so the model is less likely to invent numbers.

## Key design choice

The LLM does not get authority to decide facts. Python computes facts; the LLM explains them. This is a simple but important grounding boundary.

## What I would add next

- SQL generation against a read-only database
- Semantic metric definitions
- RAG for company documents
- Row-level access control
- Evaluation suite for groundedness, correctness, and latency
- FastAPI service + Docker deployment
