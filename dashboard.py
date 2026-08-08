import os
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

import api_queries
import transformation

load_dotenv()

st.set_page_config(page_title="Revenue Dashboard", layout="wide")
st.title("Machine Revenue Dashboard")
st.caption("Stripe revenue, fees, and net earnings — last 30 days")

api_key = os.getenv("STRIPE_API_KEY")

if not api_key:
    st.error("STRIPE_API_KEY is not configured.")
    st.stop()


@st.cache_data(ttl=900)
def load_revenue_data():
    stripe_data = api_queries.data_retrieval(api_key)
    return transformation.transform(stripe_data, api_key)


data = load_revenue_data()
df = pd.DataFrame(data)

if df.empty:
    st.warning("No successful payments were found.")
    st.stop()

# Amounts are stored in pence; convert only for display.
df["gross_gbp"] = df["amount"] / 100
df["fee_gbp"] = df["stripe_fee"] / 100
df["net_gbp"] = df["net_amount"] / 100

summary = (
    df.groupby("machine", as_index=False)
    .agg(
        gross_gbp=("gross_gbp", "sum"),
        fee_gbp=("fee_gbp", "sum"),
        net_gbp=("net_gbp", "sum"),
        transactions=("machine", "size"),
    )
    .sort_values("net_gbp", ascending=False)
)

gross = summary["gross_gbp"].sum()
fees = summary["fee_gbp"].sum()
net = summary["net_gbp"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Gross sales", f"£{gross:,.2f}")
col2.metric("Stripe fees", f"£{fees:,.2f}")
col3.metric("Net revenue", f"£{net:,.2f}")

chart = px.bar(
    summary,
    x="machine",
    y="net_gbp",
    text_auto=".2f",
    title="Net revenue by machine",
    labels={"machine": "Machine", "net_gbp": "Net revenue (£)"},
)
st.plotly_chart(chart, width='stretch')

st.subheader("Machine breakdown")
st.dataframe(
    summary,
    width='stretch',
    hide_index=True,
    column_config={
        "gross_gbp": st.column_config.NumberColumn("Gross (£)", format="£%.2f"),
        "fee_gbp": st.column_config.NumberColumn("Stripe fees (£)", format="£%.2f"),
        "net_gbp": st.column_config.NumberColumn("Net (£)", format="£%.2f"),
        "transactions": st.column_config.NumberColumn("Transactions"),
    },
)

st.download_button(
    "Download CSV",
    data=summary.to_csv(index=False),
    file_name="machine_revenue.csv",
    mime="text/csv",
)