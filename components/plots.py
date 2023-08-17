import streamlit as sl
import plotly.graph_objects as go
import plotly.express as px
import duckdb as db
from millify import millify


@sl.cache_data
def plot_metric(
    label, value, series=None, prefix="", suffix="", show_graph=False, color_graph=""
):
    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=value,
            gauge={"axis": {"visible": False}},
            number={
                "prefix": prefix,
                "suffix": suffix,
                "font.size": 28,
                "font.color": "white",
            },
            title={
                "text": label,
                "font": {"size": 24, "color": "white"},
            },
        )
    )

    if show_graph:
        fig.add_trace(
            go.Scatter(
                y=series,
                hoverinfo="skip",
                fill="tozeroy",
                fillcolor=color_graph,
                line={
                    "color": color_graph,
                },
            )
        )

    fig.update_xaxes(visible=False, fixedrange=True)
    fig.update_yaxes(visible=False, fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        margin=dict(t=30, b=0),
        showlegend=False,
        # plot_bgcolor="black",
        height=100,
    )

    sl.plotly_chart(fig, use_container_width=True)


@sl.cache_data
def plot_transact_by_day(df):
    daily_transtn = db.sql(
        f"""
        WITH aggregate_transantn AS (
            SELECT
                Day_Name AS Day,
                Day_Number,
                COUNT(SalesKey) AS Transactions
            FROM
                df
            GROUP BY 
                Day_Name, 
                Day_Number
            ORDER BY Day_Number ASC
        )

        SELECT * FROM aggregate_transantn
        """
    ).df()

    fig = px.line(
        daily_transtn,
        x="Day",
        y="Transactions",
        markers=True,
        text="Transactions",
        title="Total Transactions by Day",
    )
    sl.plotly_chart(fig, use_container_width=True)


@sl.cache_data
def plot_sales_by_day(df):
    daily_sales = db.sql(
        f"""
        WITH aggregate_sales AS (
            SELECT
                Year,
                Day_Name AS Day,
                Day_Number,
                SUM(SaleAmount) AS Sales
            FROM
                df
            GROUP BY 
                Year,
                Day_Name, 
                Day_Number
            ORDER BY Day_Number ASC
        )

        SELECT * FROM aggregate_sales
        """
    ).df()

    fig = px.line(
        daily_sales,
        x="Day",
        y="Sales",
        markers=True,
        color="Year",
        title="Total Sales by Day",
    )
    sl.plotly_chart(fig, use_container_width=True)
