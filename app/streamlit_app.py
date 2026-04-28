import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import streamlit as st
from src.db import load_csv
from src.kpi_engine import get_kpi_summary, supplier_risk_table, stockout_risk_table, monthly_spend
from src.ai_agent import ask_agent

st.set_page_config(page_title="AI Supply Chain Control Tower Agent", layout="wide")

st.title("AI Supply Chain Control Tower Agent")
st.caption("GPT-5.5 + Python + PostgreSQL-ready data + Streamlit + Power BI portfolio project")

try:
    df = load_csv()
except Exception as e:
    st.error(f"Unable to load dataset: {e}")
    st.stop()

kpis = get_kpi_summary(df)

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Spend", f"${kpis['total_spend']:,.0f}")
col2.metric("Total Orders", f"{kpis['total_orders']}")
col3.metric("Late Delivery %", f"{kpis['late_delivery_rate_pct']}%")
col4.metric("Defect %", f"{kpis['defect_rate_pct']}%")
col5.metric("Avg Lead Time", f"{kpis['avg_lead_time_days']} days")

st.divider()

left, right = st.columns([1.1, 1])

with left:
    st.subheader("Ask the AI Control Tower")
    example_questions = [
        "Which suppliers are high risk and why?",
        "Which products have stockout risk?",
        "Give me an executive summary of supply chain performance.",
        "Draft an email to a supplier with repeated late deliveries.",
        "What procurement cost-saving opportunities should leadership review?",
    ]
    selected = st.selectbox("Example questions", example_questions)
    question = st.text_area("Your question", value=selected, height=120)

    if st.button("Ask Agent", type="primary"):
        with st.spinner("Analyzing supply chain data..."):
            answer = ask_agent(question)
        st.markdown(answer)

with right:
    st.subheader("Supplier Risk Scorecard")
    st.dataframe(supplier_risk_table(df).head(10), use_container_width=True)

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.subheader("Stockout Risk")
    st.dataframe(stockout_risk_table(df).head(15), use_container_width=True)

with c2:
    st.subheader("Monthly Procurement Spend")
    spend = monthly_spend(df)
    st.line_chart(spend.set_index("month")["total_spend"])

st.divider()

st.subheader("Raw Data Preview")
st.dataframe(df.head(50), use_container_width=True)
