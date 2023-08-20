import streamlit as sl
import plotly.graph_objects as go
import plotly.express as px
import duckdb as db
from millify import millify


@sl.cache_data
def plot_gsales_metric(
    label=None,
    prefix="",
    suffix="",
    data=None,
    show_graph=True,
    show_bar=True,
    color_graph="",
):
    if data is not None:
        gross_sales = data["SaleAmount"].sum()
        sales = db.sql(
            f"""
            SELECT
                Month,
                Month_Number,
                sum(SaleAmount) as sales
            from data
            Group by Month, Month_Number
            Order by Month_Number
            """
        ).df()

        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                value=gross_sales,
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
            if show_bar:
                fig.add_trace(
                    go.Bar(
                        x=sales.Month,
                        y=sales.sales,
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=sales.Month,
                        y=sales.sales,
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
def plot_nsales_metric(
    label=None,
    prefix="",
    suffix="",
    data=None,
    show_graph=True,
    show_bar=True,
    color_graph="",
):
    if data is not None:
        net_sales = data["SaleAmount"].sum() - data["ReturnAmount"].sum()
        n_sales = db.sql(
            f"""
            SELECT
                Month,
                Month_Number,
                sum((SaleAmount - ReturnAmount)) as sales
            from data
            Group by Month, Month_Number
            Order by Month_Number
            """
        ).df()

        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                value=net_sales,
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
            if show_bar:
                fig.add_trace(
                    go.Bar(
                        x=n_sales.Month,
                        y=n_sales.sales,
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=n_sales.Month,
                        y=n_sales.sales,
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
def plot_trans_metric(
    label=None,
    prefix="",
    suffix="",
    data=None,
    show_graph=True,
    show_bar=True,
    color_graph="",
):
    if data is not None:
        num_trans = data["SalesKey"].count()
        n_trans = db.sql(
            f"""
            SELECT
                Month,
                Month_Number,
                count(SalesKey) as transactions
            from data
            Group by Month, Month_Number
            Order by Month_Number
            """
        ).df()

        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                value=num_trans,
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
            if show_bar:
                fig.add_trace(
                    go.Bar(
                        x=n_trans.Month,
                        y=n_trans.transactions,
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=n_trans.Month,
                        y=n_trans.transactions,
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
def plot_actual_trans_metric(
    label=None,
    prefix="",
    suffix="",
    data=None,
    show_graph=True,
    show_bar=True,
    color_graph="",
):
    if data is not None:
        actual_trans = data[data["ReturnAmount"] == 0]["SalesKey"].count()
        a_trans = db.sql(
            f"""
            SELECT
                Month,
                Month_Number,
                count(SalesKey) as transactions
            from data
            where ReturnAmount = 0
            Group by Month, Month_Number
            Order by Month_Number
            """
        ).df()

        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                value=actual_trans,
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
            if show_bar:
                fig.add_trace(
                    go.Bar(
                        x=a_trans.Month,
                        y=a_trans.transactions,
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=a_trans.Month,
                        y=a_trans.transactions,
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
def plot_metric(
    label,
    value,
    x=None,
    y=None,
    prefix="",
    suffix="",
    show_bar=False,
    show_graph=False,
    color_graph="",
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
        if show_bar:
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=y,
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
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
    fig.update_xaxes(visible=True, title="", fixedrange=True)
    fig.update_yaxes(visible=True, title="", fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        # margin=dict(b=0),
        # showlegend=False,
        # plot_bgcolor="black",
        height=300,
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
        title="Total Revenue by Day",
    )
    fig.update_xaxes(visible=True, title="", fixedrange=True)
    fig.update_yaxes(visible=True, title="", fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        # margin=dict(b=0),
        showlegend=False,
        # plot_bgcolor="black",
        height=300,
    )

    sl.plotly_chart(fig, use_container_width=True)


@sl.cache_data
def plot_sales_by_month(df):
    monthly_sales = db.sql(
        f"""
        WITH aggregate_sales AS (
            SELECT
                Year,
                Month,
                Month_Number,
                SUM(SaleAmount) AS Sales
            FROM
                df
            GROUP BY 
                Year,
                Month,
                Month_Number
            ORDER BY Month_Number ASC
        )

        SELECT * FROM aggregate_sales
        """
    ).df()

    fig = px.line(
        monthly_sales,
        x="Month",
        y="Sales",
        markers=True,
        color="Year",
        title="Total Revenue by Month",
    )
    fig.update_xaxes(visible=True, title="", fixedrange=True)
    fig.update_yaxes(visible=True, title="", fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        # margin=dict(t=0, b=0),
        showlegend=False,
        # plot_bgcolor="black",
        height=300,
    )

    sl.plotly_chart(fig, use_container_width=True)


@sl.cache_data
def plot_sales_by_category(df):

    sales = db.sql(
        f"""
        WITH aggregate_sales AS (
            SELECT
                Month,
                Month_Number,
                ProductCategoryName as category,
                SUM(SaleAmount) AS Sales
            FROM
                df
            GROUP BY 
                Month,
                Month_Number,
                ProductCategoryName
            ORDER BY Month_Number ASC
        )

        SELECT * FROM aggregate_sales
        """
    ).df()

    fig = px.line(
        sales,
        x="Month",
        y="Sales",
        color="category",
        title=f"Revenue by Product Category per Month",
    )
    fig.update_xaxes(visible=True, title="", fixedrange=True)
    fig.update_yaxes(visible=True, title="", fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        # margin=dict(t=0, b=0),
        showlegend=False,
        # plot_bgcolor="black",
        # width=200,
        height=300,
    )

    sl.plotly_chart(fig, use_container_width=True)


@sl.cache_data
def plot_profit_metric(
    label=None,
    prefix="",
    suffix="",
    data=None,
    show_graph=True,
    show_bar=True,
    color_graph="",
):
    if data is not None:
        tprofit = data["ProfitAmount"].sum()
        profit = db.sql(
            f"""
            SELECT
                Month,
                Month_Number,
                sum(ProfitAmount) as profit
            from data
            Group by Month, Month_Number
            Order by Month_Number
            """
        ).df()

        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                value=tprofit,
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
            if show_bar:
                fig.add_trace(
                    go.Bar(
                        x=profit.Month,
                        y=profit.profit,
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=profit.Month,
                        y=profit.profit,
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
def plot_profitmargin_metric(
    label=None,
    prefix="",
    suffix="",
    data=None,
    show_graph=True,
    show_bar=True,
    color_graph="",
):
    if data is not None:
        profitm = (data["ProfitAmount"].sum()) / (data["SaleAmount"].sum()) * 100
        mprofit = db.sql(
            f"""
            SELECT
                Month,
                Month_Number,
                ((sum(ProfitAmount)/sum(SaleAmount)) * 100) as profitmargin
            from data
            Group by Month, Month_Number
            Order by Month_Number
            """
        ).df()

        fig = go.Figure()

        fig.add_trace(
            go.Indicator(
                value=profitm,
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
            if show_bar:
                fig.add_trace(
                    go.Bar(
                        x=mprofit.Month,
                        y=mprofit.profitmargin,
                    )
                )
            else:
                fig.add_trace(
                    go.Scatter(
                        x=mprofit.Month,
                        y=mprofit.profitmargin,
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
def plot_profit_by_product(df):

    profit = db.sql(
        f"""
        WITH aggregate_profit AS (
            SELECT
                ProductName as product,
                SUM(ProfitAmount) AS profit
            FROM
                df
            GROUP BY 
                ProductName
            ORDER BY SUM(ProfitAmount) desc
            limit 10
        )

        SELECT * FROM aggregate_profit
        """
    ).df()

    fig = px.bar(
        profit,
        x="product",
        y="profit",
        orientation="v",
        title="Top 10 Product  by Profit",
    )
    fig.update_xaxes(visible=True, title="", fixedrange=True)
    fig.update_yaxes(visible=True, title="", fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        # margin=dict(t=0, b=0),
        # showlegend=False,
        # plot_bgcolor="black",
        # width=200,
        height=700,
    )

    sl.plotly_chart(fig, use_container_width=True)


@sl.cache_data
def plot_profit_by_category(df):

    category = db.sql(
        f"""
        WITH aggregate_profit AS (
            SELECT
                ProductCategoryName as category,
                ((sum(ProfitAmount)/sum(SaleAmount)) * 100) as profitmargin
            FROM
                df
            GROUP BY 
                ProductCategoryName
            ORDER BY ((sum(ProfitAmount)/sum(SaleAmount)) * 100) desc
        )

        SELECT * FROM aggregate_profit
        """
    ).df()

    fig = px.bar(
        category,
        x="category",
        y="profitmargin",
        orientation="v",
        title="Product Category by Profit Margin",
    )
    fig.update_xaxes(visible=True, title="", fixedrange=True)
    fig.update_yaxes(visible=True, title="", fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        # margin=dict(t=0, b=0),
        # showlegend=False,
        # plot_bgcolor="black",
        # width=200,
        height=550
    )

    sl.plotly_chart(fig, use_container_width=True)


@sl.cache_data
def plot_profit_by_month(df):

    profit = db.sql(
        f"""
        WITH aggregate_profit AS (
            SELECT
                Month,
                Month_Number,
                SUM(ProfitAmount) AS profit
            FROM
                df
            GROUP BY 
                Month, Month_Number
            ORDER BY Month_Number asc
        )

        SELECT * FROM aggregate_profit
        """
    ).df()

    fig = px.bar(
        profit,
        x="profit",
        y="Month",
        orientation="h",
        title="Profit by Month",
    )
    fig.update_xaxes(visible=True, title="", fixedrange=True)
    fig.update_yaxes(visible=True, title="", fixedrange=True)
    fig.update_layout(
        # paper_bgcolor="lightgrey",
        # margin=dict(t=0, b=0),
        # showlegend=False,
        # plot_bgcolor="black",
        # width=200,
        height=680,
    )

    sl.plotly_chart(fig, use_container_width=True)
