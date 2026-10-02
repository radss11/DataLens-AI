from __future__ import annotations
import re
from typing import Any
import numpy as np
import pandas as pd


def _find_col(df: pd.DataFrame, terms: list[str]) -> str | None:
    for c in df.columns:
        n = re.sub(r"[^a-z0-9]", "", c.lower())
        if any(t in n for t in terms):
            return c
    return None


def summarize(df: pd.DataFrame) -> dict[str, Any]:
    numeric = df.select_dtypes(include="number")
    out: dict[str, Any] = {
        "rows": len(df),
        "columns": len(df.columns),
        "missing_cells": int(df.isna().sum().sum()),
        "duplicates": int(df.duplicated().sum()),
        "numeric_summary": {},
    }
    for c in numeric.columns:
        s = numeric[c].dropna()
        if len(s):
            out["numeric_summary"][c] = {
                "mean": float(s.mean()), "median": float(s.median()),
                "min": float(s.min()), "max": float(s.max())
            }
    return out


def trend(df: pd.DataFrame) -> dict[str, Any] | None:
    year = _find_col(df, ["year", "date", "time"])
    numeric = df.select_dtypes(include="number").columns.tolist()
    if not year or not numeric:
        return None
    candidates = [c for c in numeric if c != year]
    if not candidates:
        return None
    y = candidates[0]
    g = df[[year, y]].dropna().groupby(year, as_index=False)[y].mean()
    if len(g) < 2:
        return None
    first, last = float(g[y].iloc[0]), float(g[y].iloc[-1])
    change = None if first == 0 else (last - first) / abs(first) * 100
    return {"dimension": year, "metric": y, "first": first, "last": last,
            "pct_change": change, "table": g.to_dict("records")}


def group_insight(df: pd.DataFrame, question: str) -> dict[str, Any] | None:
    categorical = df.select_dtypes(exclude="number").columns.tolist()
    numeric = df.select_dtypes(include="number").columns.tolist()
    if not categorical or not numeric:
        return None
    q = question.lower()
    group_terms = ["by ", "compare", "comparison", "which", "top ", "highest", "lowest", "average", "group", "region", "country", "continent", "category"]
    if not any(t in q for t in group_terms):
        return None
    # Prefer explicitly named categorical columns from the question.
    group = next((c for c in categorical if c.lower() in q), categorical[0])
    metric = next((c for c in numeric if c.lower() in q), numeric[0])
    g = (df.groupby(group, dropna=False)[metric].agg(["mean", "sum", "count"])
           .sort_values("mean", ascending=False).reset_index())
    if g.empty:
        return None
    return {"group": group, "metric": metric, "rows": g.head(10).to_dict("records")}


def answer_locally(df: pd.DataFrame, question: str) -> dict[str, Any]:
    """Deterministic analyst used when no LLM key is configured."""
    s = summarize(df)
    tr = trend(df)
    gi = group_insight(df, question)
    insights = []
    if tr and tr["pct_change"] is not None:
        direction = "increased" if tr["pct_change"] >= 0 else "decreased"
        insights.append(f"Average {tr['metric']} {direction} by {abs(tr['pct_change']):.1f}% from the first to last {tr['dimension']} in the loaded data.")
    if gi and gi["rows"]:
        top = gi["rows"][0]
        insights.append(f"The highest average {gi['metric']} is for {gi['group']}={top[gi['group']]} ({top['mean']:.2f}).")
    insights.append(f"The dataset contains {s['rows']:,} rows, {s['columns']} columns, and {s['missing_cells']:,} missing cells.")
    return {"mode": "local", "insights": insights, "profile": s, "trend": tr, "group": gi}
