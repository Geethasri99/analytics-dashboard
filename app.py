—📊─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────📊•───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"""Retail Analytics Dashboard — Streamlit + Plotly."""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date, timedelta

st.set_page_config(page_title="Retail Analytics", page_icon="📊", layout="wide")


@st.cache_data
def load_data(n: int = 5000) -> pd.DataFrame:
      rng = np.random.default_rng(42)
      start = date(2023, 1, 1)
      dates = [start + timedelta(days=int(d)) for d in rng.integers(0, 365, n)]
      return pd.DataFrame({
          "order_date": dates,
          "region": rng.choice(["North", "South", "East", "West"], n, p=[0.3, 0.25, 0.25, 0.2]),
          "category": rng.choice(["Electronics", "Apparel", "Home", "Sports", "Beauty"], n),
          "amount": np.round(rng.lognormal(4.5, 0.8, n), 2),
          "customer_id": rng.integers(1000, 2000, n),
          "status": rng.choice(
              ["delivered", "shipped", "processing", "cancelled", "returned"],
              n, p=[0.6, 0.15, 0.1, 0.1, 0.05],
          ),
      })


def tier(rev):
      if rev >= 10000: return "Platinum"
            if rev >= 5000: return "Gold"
                  if rev >= 1000: return "Silver"
                        return "Bronze"


df = load_data()

st.sidebar.header("Filters")
regions = st.sidebar.multiselect("Region", df["region"].unique(), default=list(df["region"].unique()))
cats = st.sidebar.multiselect("Category", df["category"].unique(), default=list(df["category"].unique()))
statuses = st.sidebar.multiselect("Status", df["status"].unique(), default=["delivered", "shipped", "processing"])

f = df[df["region"].isin(regions) & df["category"].isin(cats) & df["status"].isin(statuses)]

st.title("Retail Analytics Dashboard")
if f.empty:
      st.warning("No data for selected filters.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Revenue", f"${f['amount'].sum():,.0f}")
k2.metric("Orders", f"{len(f):,}")
k3.metric("Avg Order", f"${f['amount'].mean():,.2f}")
k4.metric("Customers", f"{f['customer_id'].nunique():,}")

st.divider()
col1, col2 = st.columns(2)

with col1:
      st.subheader("Monthly Revenue Trend")
    monthly = f.assign(month=pd.to_datetime(f["order_date"]).dt.to_period("M").dt.to_timestamp()).groupby("month")["amount"].sum().reset_index()
    st.plotly_chart(px.area(monthly, x="month", y="amount", labels={"amount": "Revenue ($)", "month": ""}), use_container_width=True)

with col2:
      st.subheader("Revenue by Category")
    cat_rev = f.groupby("category")["amount"].sum().reset_index().sort_values("amount")
    st.plotly_chart(px.bar(cat_rev, x="amount", y="category", orientation="h", labels={"amount": "Revenue ($)", "category": ""}), use_container_width=True)

col3, col4 = st.columns(2)

with col3:
      st.subheader("Revenue by Region")
    reg = f.groupby("region")["amount"].sum().reset_index()
    st.plotly_chart(px.pie(reg, names="region", values="amount", hole=0.4), use_container_width=True)

with col4:
      st.subheader("Customer Segments")
    segs = f.groupby("customer_id")["amount"].sum().apply(tier).value_counts().reset_index()
    segs.columns = ["Tier", "Count"]
    colors = {"Bronze": "#cd7f32", "Silver": "#c0c0c0", "Gold": "#ffd700", "Platinum": "#e5e4e2"}
    st.plotly_chart(px.bar(segs, x="Tier", y="Count", color="Tier", color_discrete_map=colors), use_container_width=True)

with st.expander("Raw data"):
      st.dataframe(f.sort_values("order_date", ascending=False).head(500), use_container_width=True)
