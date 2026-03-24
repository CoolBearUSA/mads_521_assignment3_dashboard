import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

st.title("School Spending Dashboard")

# -----------------------------
# Load Data
# -----------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("LEA_Transactional_Report_cleaned.csv")
    return df


df = load_data()

# -----------------------------
# Filters
# -----------------------------
st.sidebar.header("Filters")

district = st.sidebar.selectbox(
    "District",
    ["All"] + sorted(df["Description Level"].unique())
)

school = st.sidebar.selectbox(
    "School Year",
    ["All"] + sorted(df["School Year"].unique())
)

year = st.sidebar.selectbox(
    "Object Description",
    ["All"] + sorted(df["Object Description"].unique())
)

# Apply filters
filtered_df = df.copy()

if district != "All":
    filtered_df = filtered_df[filtered_df["Description Level"] == district]

if school != "All":
    filtered_df = filtered_df[filtered_df["School Year"] == school]

if year != "All":
    filtered_df = filtered_df[filtered_df["Object Description"] == year]

# -----------------------------
# 1. Spending Over Time (Line)
# -----------------------------

time_data = (
    filtered_df
    .groupby("year_month")["amount"]
    .sum()
    .reset_index()
)

# Plotly line chart
fig = px.line(
    time_data,
    x="year_month",
    y="amount",
    title="Spending Over Time",
    labels={"amount": "Amount", "year_month": "Month-Year"}
)
st.plotly_chart(fig)

# -----------------------------
# 2. Spending by School (Bar)
# -----------------------------

school_data = (
    filtered_df
    .groupby("School Name")["amount"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

fig2 = px.bar(
    school_data,
    x="School Name",
    y="amount",
    title="Spending by School"
)
# Increase figure height
fig2.update_layout(
    height=800,           # increase height
    width=1200,           # optional: increase width
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# 3. Spending by Object (Stacked Bar by Month)
# -----------------------------

stacked_data = (
    filtered_df.groupby(["year_month", "Object Description"])["amount"]
    .sum()
    .reset_index()
)

fig = px.bar(
    stacked_data,
    x="year_month",          # now exists
    y="amount",
    color="Object Description",
    title="Spending by Object",
    labels={"amount": "Amount", "year_month": "Month-Year"},
    barmode="stack"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Raw Data (Optional)
# -----------------------------
st.subheader("Raw Data")
st.dataframe(filtered_df)