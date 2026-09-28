
import pandas as pd
import streamlit as st
import plotly.express as px


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="Interactive Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# Page Header
# =========================================================

st.title("📊 Interactive Analytics Dashboard")

st.write(
    "Explore sales, profit, customers, products, and trends "
    "using interactive filters and visualizations."
)


# =========================================================
# Load Data
# =========================================================

df = pd.read_excel(
    "data/sample_-_superstore.xls",
    engine="xlrd"
)


# =========================================================
# Prepare Data
# =========================================================

df["Order Date"] = pd.to_datetime(df["Order Date"])

df["Month"] = df["Order Date"].dt.to_period("M")


# =========================================================
# Sidebar Filters
# =========================================================

st.sidebar.header("🔎 Filters")


def reset_filters():
    """Reset all dashboard filters to their default values."""

    st.session_state.region = "All"
    st.session_state.category = "All"
    st.session_state.segment = "All"
    st.session_state.sub_category = "All"

    st.session_state.date_range = (
        df["Order Date"].min().date(),
        df["Order Date"].max().date()
    )


# -----------------------------
# Region
# -----------------------------

regions = ["All"] + sorted(
    df["Region"].unique().tolist()
)

region = st.sidebar.selectbox(
    "Select Region",
    regions,
    key="region"
)


# -----------------------------
# Category
# -----------------------------

categories = ["All"] + sorted(
    df["Category"].unique().tolist()
)

category = st.sidebar.selectbox(
    "Select Category",
    categories,
    key="category"
)


# -----------------------------
# Customer Segment
# -----------------------------

segments = ["All"] + sorted(
    df["Segment"].unique().tolist()
)

segment = st.sidebar.selectbox(
    "Select Customer Segment",
    segments,
    key="segment"
)


# -----------------------------
# Sub-Category
# -----------------------------

sub_categories = ["All"] + sorted(
    df["Sub-Category"].unique().tolist()
)

sub_category = st.sidebar.selectbox(
    "Select Sub-Category",
    sub_categories,
    key="sub_category"
)


# -----------------------------
# Date Range
# -----------------------------

date_range = st.sidebar.date_input(
    "Select Date Range",
    [
        df["Order Date"].min().date(),
        df["Order Date"].max().date()
    ],
    key="date_range"
)


# -----------------------------
# Reset Button
# -----------------------------

st.sidebar.button(
    "Reset Filters",
    on_click=reset_filters,
    use_container_width=True
)


# =========================================================
# Apply Filters
# =========================================================

filtered_df = df


if region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == region
    ]


if category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == category
    ]


if segment != "All":
    filtered_df = filtered_df[
        filtered_df["Segment"] == segment
    ]


if sub_category != "All":
    filtered_df = filtered_df[
        filtered_df["Sub-Category"] == sub_category
    ]


if len(date_range) == 2:

    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["Order Date"].dt.date >= start_date)
        & (filtered_df["Order Date"].dt.date <= end_date)
    ]


# =========================================================
# Empty Data Check
# =========================================================

if filtered_df.empty:

    st.warning(
        "No data matches the selected filters. "
        "Try changing your filter selections."
    )

    st.stop()


# =========================================================
# Dataset Preview
# =========================================================

st.subheader("Dataset Preview")

st.dataframe(
    filtered_df.head(10),
    use_container_width=True
)


# =========================================================
# Dataset Information
# =========================================================

st.subheader("Dataset Information")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Number of Rows",
        f"{len(filtered_df):,}"
    )

with col2:

    st.metric(
        "Number of Columns",
        f"{len(filtered_df.columns):,}"
    )


# =========================================================
# Key Metrics
# =========================================================

st.subheader("Key Metrics")


total_sales = filtered_df["Sales"].sum()

total_profit = filtered_df["Profit"].sum()

total_orders = filtered_df["Order ID"].nunique()

average_order_value = (
    total_sales / total_orders
    if total_orders > 0
    else 0
)

profit_margin = (
    (total_profit / total_sales) * 100
    if total_sales != 0
    else 0
)


col1, col2, col3, col4, col5 = st.columns(5)


with col1:

    st.metric(
        "Total Sales",
        f"${total_sales:,.2f}"
    )


with col2:

    st.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )


with col3:

    st.metric(
        "Total Orders",
        f"{total_orders:,}"
    )


with col4:

    st.metric(
        "Average Order Value",
        f"${average_order_value:,.2f}"
    )


with col5:

    st.metric(
        "Profit Margin",
        f"{profit_margin:.2f}%"
    )


# =========================================================
# Sales Over Time
# =========================================================

st.subheader("Sales Over Time")


sales_over_time = (
    filtered_df
    .groupby("Order Date")["Sales"]
    .sum()
    .reset_index()
)


fig_sales_time = px.line(
    sales_over_time,
    x="Order Date",
    y="Sales",
    title="Daily Sales",
    markers=True,
    hover_data={
        "Order Date": True,
        "Sales": ":$,.2f"
    }
)


fig_sales_time.update_layout(
    xaxis_title="Order Date",
    yaxis_title="Sales ($)",
    hovermode="x unified"
)


st.plotly_chart(
    fig_sales_time,
    use_container_width=True,
    key="sales_over_time"
)


# =========================================================
# Category Analysis
# =========================================================

st.subheader("Category Analysis")

col1, col2 = st.columns(2)


# -----------------------------
# Sales by Category
# -----------------------------

with col1:

    sales_by_category = (
        filtered_df
        .groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )


    fig_category = px.bar(
        sales_by_category,
        x="Category",
        y="Sales",
        title="Sales by Category",
        text="Sales",
        hover_data={
            "Category": True,
            "Sales": ":$,.2f"
        }
    )


    fig_category.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )


    fig_category.update_layout(
        xaxis_title="Category",
        yaxis_title="Sales ($)"
    )


    st.plotly_chart(
        fig_category,
        use_container_width=True,
        key="sales_by_category"
    )


# -----------------------------
# Profit by Category
# -----------------------------

with col2:

    profit_by_category = (
        filtered_df
        .groupby("Category")["Profit"]
        .sum()
        .reset_index()
    )


    fig_profit_category = px.bar(
        profit_by_category,
        x="Category",
        y="Profit",
        title="Profit by Category",
        text="Profit",
        hover_data={
            "Category": True,
            "Profit": ":$,.2f"
        }
    )


    fig_profit_category.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )


    fig_profit_category.update_layout(
        xaxis_title="Category",
        yaxis_title="Profit ($)"
    )


    st.plotly_chart(
        fig_profit_category,
        use_container_width=True,
        key="profit_by_category"
    )


# =========================================================
# Sales by Region
# =========================================================

st.subheader("Sales by Region")


sales_by_region = (
    filtered_df
    .groupby("Region")["Sales"]
    .sum()
    .reset_index()
)


fig_region = px.bar(
    sales_by_region,
    x="Region",
    y="Sales",
    title="Sales by Region",
    text="Sales",
    hover_data={
        "Region": True,
        "Sales": ":$,.2f"
    }
)


fig_region.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)


fig_region.update_layout(
    xaxis_title="Region",
    yaxis_title="Sales ($)"
)


st.plotly_chart(
    fig_region,
    use_container_width=True,
    key="sales_by_region"
)


# =========================================================
# Customer Segment Analysis
# =========================================================

st.subheader("Customer Segment Analysis")

col1, col2 = st.columns(2)


# -----------------------------
# Sales by Customer Segment
# -----------------------------

with col1:

    sales_by_segment = (
        filtered_df
        .groupby("Segment")["Sales"]
        .sum()
        .reset_index()
    )


    fig_segment = px.bar(
        sales_by_segment,
        x="Segment",
        y="Sales",
        title="Sales by Customer Segment",
        text="Sales",
        hover_data={
            "Segment": True,
            "Sales": ":$,.2f"
        }
    )


    fig_segment.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )


    fig_segment.update_layout(
        xaxis_title="Customer Segment",
        yaxis_title="Sales ($)"
    )


    st.plotly_chart(
        fig_segment,
        use_container_width=True,
        key="sales_by_segment"
    )


# -----------------------------
# Profit by Customer Segment
# -----------------------------

with col2:

    profit_by_segment = (
        filtered_df
        .groupby("Segment")["Profit"]
        .sum()
        .reset_index()
    )


    fig_profit_segment = px.bar(
        profit_by_segment,
        x="Segment",
        y="Profit",
        title="Profit by Customer Segment",
        text="Profit",
        hover_data={
            "Segment": True,
            "Profit": ":$,.2f"
        }
    )


    fig_profit_segment.update_traces(
        texttemplate="$%{text:,.0f}",
        textposition="outside"
    )


    fig_profit_segment.update_layout(
        xaxis_title="Customer Segment",
        yaxis_title="Profit ($)"
    )


    st.plotly_chart(
        fig_profit_segment,
        use_container_width=True,
        key="profit_by_segment"
    )


# =========================================================
# Top 10 Products
# =========================================================

st.subheader("Top 10 Products by Sales")


top_products = (
    filtered_df
    .groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=True)
    .tail(10)
    .reset_index()
)


fig_products = px.bar(
    top_products,
    x="Sales",
    y="Product Name",
    orientation="h",
    title="Top 10 Products by Sales",
    text="Sales",
    hover_data={
        "Product Name": True,
        "Sales": ":$,.2f"
    }
)


fig_products.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)


fig_products.update_layout(
    xaxis_title="Sales ($)",
    yaxis_title="Product"
)


st.plotly_chart(
    fig_products,
    use_container_width=True,
    key="top_products"
)


# =========================================================
# Monthly Trends
# =========================================================

st.subheader("Monthly Trends")

col1, col2 = st.columns(2)


# -----------------------------
# Monthly Sales
# -----------------------------

with col1:

    monthly_sales = (
        filtered_df
        .groupby("Month")["Sales"]
        .sum()
        .reset_index()
    )


    monthly_sales["Month"] = (
        monthly_sales["Month"].astype(str)
    )


    fig_monthly_sales = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        title="Monthly Sales Trend",
        markers=True,
        hover_data={
            "Month": True,
            "Sales": ":$,.2f"
        }
    )


    fig_monthly_sales.update_layout(
        xaxis_title="Month",
        yaxis_title="Sales ($)",
        hovermode="x unified"
    )


    st.plotly_chart(
        fig_monthly_sales,
        use_container_width=True,
        key="monthly_sales"
    )


# -----------------------------
# Monthly Profit
# -----------------------------

with col2:

    monthly_profit = (
        filtered_df
        .groupby("Month")["Profit"]
        .sum()
        .reset_index()
    )


    monthly_profit["Month"] = (
        monthly_profit["Month"].astype(str)
    )


    fig_monthly_profit = px.line(
        monthly_profit,
        x="Month",
        y="Profit",
        title="Monthly Profit Trend",
        markers=True,
        hover_data={
            "Month": True,
            "Profit": ":$,.2f"
        }
    )


    fig_monthly_profit.update_layout(
        xaxis_title="Month",
        yaxis_title="Profit ($)",
        hovermode="x unified"
    )


    st.plotly_chart(
        fig_monthly_profit,
        use_container_width=True,
        key="monthly_profit"
    )


# =========================================================
# Sales vs Profit
# =========================================================

st.subheader("Sales vs Profit")


sales_profit = (
    filtered_df
    .groupby("Category")[["Sales", "Profit"]]
    .sum()
    .reset_index()
)


fig_sales_profit = px.scatter(
    sales_profit,
    x="Sales",
    y="Profit",
    size="Sales",
    title="Sales vs Profit by Category",
    text="Category",
    hover_data={
        "Category": True,
        "Sales": ":$,.2f",
        "Profit": ":$,.2f"
    }
)


fig_sales_profit.update_layout(
    xaxis_title="Sales ($)",
    yaxis_title="Profit ($)"
)


st.plotly_chart(
    fig_sales_profit,
    use_container_width=True,
    key="sales_vs_profit"
)