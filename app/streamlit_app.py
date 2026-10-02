from __future__ import annotations
import os, sys
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
sys.path.insert(0, str(ROOT / "src"))
from datalens_ai.data import load_dataset, profile_dataset
from datalens_ai.agent import answer

st.set_page_config(page_title="DataLens AI", page_icon="📊", layout="wide")
st.title("📊 DataLens AI")
st.caption("Grounded GenAI for data exploration and decision intelligence")

with st.sidebar:
    st.header("Data source")
    upload = st.file_uploader("Upload a CSV", type=["csv"])
    st.write("Default dataset: Gapminder global development data")
    st.info("The bundled dataset is real published data distributed through Plotly Express. No synthetic rows are generated.")

try:
    if upload:
        df = pd.read_csv(upload)
    else:
        df = load_dataset()
except Exception as e:
    st.error(str(e)); st.stop()

p = profile_dataset(df)
c1,c2,c3,c4 = st.columns(4)
c1.metric("Rows", f"{p['rows']:,}")
c2.metric("Columns", p['columns'])
c3.metric("Missing cells", f"{p['missing_cells']:,}")
c4.metric("Duplicate rows", f"{p['duplicate_rows']:,}")

st.subheader("Explore")
num = df.select_dtypes(include="number").columns.tolist()
cat = df.select_dtypes(exclude="number").columns.tolist()
if num:
    left,right=st.columns(2)
    with left:
        x = st.selectbox("X axis", df.columns, index=0)
    with right:
        y = st.selectbox("Y axis", num, index=0)
    color = st.selectbox("Color (optional)", ["None"] + cat)
    kwargs = {} if color == "None" else {"color": color}
    fig = px.scatter(df, x=x, y=y, **kwargs, hover_data=df.columns[:min(6,len(df.columns))])
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Ask DataLens AI")
q = st.text_input("Ask a data question", placeholder="What are the biggest changes over time, and where should I investigate further?")
if q:
    with st.spinner("Computing evidence and generating grounded analysis…"):
        result = answer(df, q)
    st.markdown("### Answer")
    st.markdown(result.get("llm_answer", ""))
    if result.get("mode") == "gemini-grounded":
        st.caption("GenAI response grounded only in computed dataset evidence.")
    else:
        st.caption("Local evidence mode: configure GEMINI_API_KEY for GenAI narrative generation.")
    with st.expander("Show evidence used by the analyst"):
        st.json({k:v for k,v in result.items() if k not in {"llm_answer"}})

with st.expander("Dataset preview"):
    st.dataframe(df.head(50), use_container_width=True)
