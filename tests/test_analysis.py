import sys
sys.path.insert(0, "src")
import pandas as pd
from datalens_ai.analysis import summarize, trend, group_insight

def test_summary_counts():
    df = pd.DataFrame({"year":[2020,2021,2022], "value":[10,20,30], "region":["A","A","B"]})
    s=summarize(df)
    assert s["rows"]==3
    assert s["columns"]==3
    assert s["missing_cells"]==0

def test_trend():
    df=pd.DataFrame({"year":[2020,2021,2022],"value":[10,20,30]})
    t=trend(df)
    assert round(t["pct_change"],1)==200.0

def test_group_insight():
    df=pd.DataFrame({"region":["A","A","B"],"value":[10,40,20]})
    g=group_insight(df,"compare region")
    assert g["rows"][0]["region"]=="A"
