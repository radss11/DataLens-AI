# DataLens AI — GenAI-Powered Data Analytics & Decision Intelligence

DataLens AI is a Python application that turns structured datasets into evidence-grounded analytical answers. It combines deterministic data analysis with optional GenAI narrative generation.

## Why this project

The design targets enterprise Data & AI use cases: conversational analytics, data-driven decision support, explainable insights, and a clear separation between computation and language generation.

## Features

- Real bundled dataset: Gapminder country-year data (1,704 rows)
- CSV upload for arbitrary tabular datasets
- Automatic data profiling
- Interactive Plotly exploration
- Trend analysis and group-level comparisons
- Grounded GenAI using Gemini (optional)
- Local TF-IDF retrieval over documented project/domain context
- Deterministic fallback when no API key is available
- Evidence panel showing what the model was allowed to use
- Tests for analytical components

## Architecture

```text
                 ┌────────────────────┐
                 │ Streamlit UI       │
                 └─────────┬──────────┘
                           │
                    CSV / Question
                           │
                 ┌─────────▼──────────┐
                 │ Data Loader        │
                 │ + Profiler         │
                 └─────────┬──────────┘
                           │
                 ┌─────────▼──────────┐
                 │ Deterministic      │
                 │ Analysis Engine    │
                 └─────────┬──────────┘
                           │ computed evidence
                 ┌─────────▼──────────┐
                 │ Grounded GenAI     │
                 │ Gemini (optional)  │
                 └─────────┬──────────┘
                           │
                 ┌─────────▼──────────┐
                 │ Answer + Evidence  │
                 └────────────────────┘
```

## Run locally

### 1. Create environment

```bash
python -m venv .venv
# Windows PowerShell
.venv\\Scripts\\Activate.ps1
# macOS/Linux
source .venv/bin/activate
```

### 2. Install

```bash
pip install -r requirements.txt
```

### 3. Start

```bash
streamlit run app/streamlit_app.py
```

The app works without an API key in deterministic/local mode.

### 4. Optional FastAPI service

```bash
uvicorn api.main:app --reload
```

Then open `http://127.0.0.1:8000/docs`.

### 5. Enable GenAI

Copy `.env.example` to `.env` and set:

```text
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-2.5-flash
```

Then restart Streamlit.

## Test

```bash
pytest -q
```

