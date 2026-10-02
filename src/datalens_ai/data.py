from __future__ import annotations
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA = ROOT / "data" / "gapminder.csv"


def load_dataset(path: str | Path | None = None) -> pd.DataFrame:
    """Load CSV and perform conservative type normalization.

    No rows are fabricated or silently dropped. Only obvious date parsing is
    attempted when a column name contains 'date'.
    """
    file_path = Path(path) if path else DEFAULT_DATA
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found: {file_path}")
    df = pd.read_csv(file_path)
    for col in df.columns:
        if "date" in col.lower():
            parsed = pd.to_datetime(df[col], errors="coerce")
            if parsed.notna().mean() >= 0.8:
                df[col] = parsed
    return df


def profile_dataset(df: pd.DataFrame) -> dict:
    numeric = df.select_dtypes(include="number")
    categorical = df.select_dtypes(exclude="number")
    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "missing_cells": int(df.isna().sum().sum()),
        "numeric_columns": list(numeric.columns),
        "categorical_columns": list(categorical.columns),
        "duplicate_rows": int(df.duplicated().sum()),
    }
