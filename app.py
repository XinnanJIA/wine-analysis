import streamlit as sl
import pandas as pd
from streamlit_option_menu import option_menu
from millify import millify
from components.plots import plot_metric, plot_transact_by_day, plot_sales_by_day
import duckdb as db

# from pathlib import Path
from components.css import css

# import os

# cwd = Path(__file__).parent

# ========= Page setup ======================
sl.set_page_config(page_title="Sales Dashboard", page_icon=":bar_chart:", layout="wide")

# go to webfx.com/tools/emoji-cheat-sheet/ for emoji's

# ========= Fetch data from the database ===============

# read data from created json file
# @sl.cache_data
# def read_csv(f):
#     return pd.read_csv(f"{f}")

# ========= CSS ===============
sl.markdown(css, unsafe_allow_html=True)

# read data from database
@sl.cache_data
def fetch_data():
    from components.mysql import contosodb

    data = pd.read_sql_query("select * from fsale limit 50000", contosodb)
    # data.to_csv(f"{cwd}\\query.csv", index=False)

    return data


# check if the data json file has been created
# for f in os.listdir():
#     if f == "query.csv":
#         datafile = f
#         break
#     else:
#         datafile = None

# if json file does not exist, fetch data from database
# if datafile is None:
#     data = fetch_data()
# else:
#     data = read_csv(datafile)

data = fetch_data()

# create new date metadata columns
data["Year"] = data["DateKey"].dt.year
data["Month"] = data["DateKey"].dt.month_name()
data["Month_Number"] = data["DateKey"].dt.month
data["Day_Name"] = data["DateKey"].dt.day_name()
data["Day_Number"] = data["DateKey"].dt.day_name()

# create day number column.
data["Day_Number"].replace(
    ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    [1, 2, 3, 4, 5, 6, 7],
    inplace=True,
)

sl.header("Consoto Sale's Dashboard :bar_chart:")
with sl.sidebar:
    selected = option_menu(
        menu_title=None,
        options=["Sales", "Profit", "Refunds"],
        icons=["receipt-cutoff", "cash-coin", "currency-dollar"],
        default_index=0,
        orientation="vertical",
    )
    "---"

year = data["Year"].unique()
year.sort()

if selected == "Sales":
    # ======== Filter Pane ======
    with sl.sidebar:
        years = sl.multiselect("Select Year", options=year, default=year)

    filtered_data = data.query("Year == @years")

    # ======= Calculate sales metrics ==========
    gross_sales = filtered_data["SaleAmount"].sum()
    sales = db.sql(
        f"""
        SELECT
            Month,
            Month_Number,
            sum(SaleAmount) as sales
        from filtered_data
        Group by Month, Month_Number
        Order by Month_Number
        """
    ).df()

    net_sales = filtered_data["SaleAmount"].sum() - filtered_data["ReturnAmount"].sum()
    n_sales = db.sql(
        f"""
        SELECT
            Month,
            Month_Number,
            sum((SaleAmount - ReturnAmount)) as sales
        from filtered_data
        Group by Month, Month_Number
        Order by Month_Number
        """
    ).df()

    num_trans = filtered_data["SalesKey"].count()
    n_trans = db.sql(
        f"""
        SELECT
            Month,
            Month_Number,
            count(SalesKey) as transactions
        from filtered_data
        Group by Month, Month_Number
        Order by Month_Number
        """
    ).df()
    actual_trans = filtered_data[filtered_data["ReturnAmount"] == 0]["SalesKey"].count()
    a_trans = db.sql(
        f"""
        SELECT
            Month,
            Month_Number,
            count(SalesKey) as transactions
        from filtered_data
        where ReturnAmount = 0
        Group by Month, Month_Number
        Order by Month_Number
        """
    ).df()

    # ======= Display Snapshots of sales =========
    gsales, nsales, trans, act_trans = sl.columns(4)
    # gsales.metric(label="**Gross Sales**", value=millify(gross_sales, precision=2))
    with gsales:
        plot_metric(
            "Gross Sales",
            value=gross_sales,
            x=sales.Month,
            y=sales.sales,
            prefix="$",
            show_graph=True,
            color_graph="rgba(0, 104, 201, 0.2)",
        )
    # nsales.metric(label="**Net Sales**", value=millify(net_sales, precision=2))
    with nsales:
        plot_metric(
            "Net Sales",
            value=net_sales,
            x=n_sales.Month,
            y=n_sales.sales,
            prefix="$",
            show_bar=True,
            show_graph=True,
            color_graph="rgba(0, 104, 201, 0.2)",
        )
    # trans.metric(label="**Total Transactions**", value=millify(num_trans))
    with trans:
        plot_metric(
            "Total Transactions",
            value=num_trans,
            x=n_trans.Month,
            y=n_trans.transactions,
            show_bar=False,
            show_graph=True,
            color_graph="rgba(0, 104, 201, 0.2)",
        )
    # act_trans.metric(label="**Actual Transactions**", value=millify(actual_trans))
    with act_trans:
        plot_metric(
            "Actual Transactions",
            value=actual_trans,
            x=a_trans.Month,
            y=a_trans.transactions,
            show_bar=True,
            show_graph=True,
            color_graph="rgba(0, 104, 201, 0.2)",
        )
    "---"
    # with sl.expander("Data Preview"):
    #     sl.dataframe(
    #         filtered_data,
    #         column_config={
    #             "Year": sl.column_config.NumberColumn(format="%d"),
    #             "SalesKey": sl.column_config.NumberColumn(format="%d"),
    #         },
    #     )
    # sl.write(sales)
    # ========= Display Charts ==================
    top_left, top_right = sl.columns(2)
    with top_left:
        plot_transact_by_day(filtered_data)

    with top_right:
        plot_sales_by_day(filtered_data)
elif selected == "Profit":
    with sl.sidebar:
        sl.multiselect("Select Year", options=year, default=year)
    sl.write("Profit")
elif selected == "Refunds":
    with sl.sidebar:
        sl.multiselect("Select Year", options=year, default=year)
    sl.write("Refunds")
