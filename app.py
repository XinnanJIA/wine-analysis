import streamlit as sl
import pandas as pd
from streamlit_option_menu import option_menu
from millify import millify
from components.plots import plot_metric

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
    sales = filtered_data["SaleAmount"]
    net_sales = filtered_data["SaleAmount"].sum() - filtered_data["ReturnAmount"].sum()
    num_trans = filtered_data["SalesKey"].count()
    actual_trans = filtered_data[filtered_data["ReturnAmount"] == 0]["SalesKey"].count()

    # ======= Display Snapshots of sales =========
    gsales, nsales, trans, act_trans = sl.columns(4)
    # gsales.metric(label="**Gross Sales**", value=millify(gross_sales, precision=2))
    with gsales:
        plot_metric(
            "Gross Sales",
            value=gross_sales,
            series=sales,
            prefix="$",
            show_graph=True,
            color_graph="rgba(0, 104, 201, 0.2)",
        )
    # nsales.metric(label="**Net Sales**", value=millify(net_sales, precision=2))
    with nsales:
        plot_metric(
            "Net Sales",
            value=net_sales,
            series=sales,
            prefix="$",
            show_graph=True,
            color_graph="rgba(0, 104, 201, 0.2)",
        )
    trans.metric(label="**Total Transactions**", value=millify(num_trans))
    act_trans.metric(label="**Actual Transactions**", value=millify(actual_trans))
    "---"
    with sl.expander("Data Preview"):
        sl.dataframe(
            filtered_data,
            column_config={
                "Year": sl.column_config.NumberColumn(format="%d"),
                "SalesKey": sl.column_config.NumberColumn(format="%d"),
            },
        )
elif selected == "Profit":
    with sl.sidebar:
        sl.multiselect("Select Year", options=year, default=year)
    sl.write("Profit")
elif selected == "Refunds":
    with sl.sidebar:
        sl.multiselect("Select Year", options=year, default=year)
    sl.write("Refunds")
