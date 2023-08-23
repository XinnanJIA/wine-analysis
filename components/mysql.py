import mysql.connector as cn
import streamlit as sl
import pandas as pd

# ====================Connect to the Database============
contosodb = cn.connect(
    host="localhost", user="root", password="ekedie", database="contoso_store"
)

# create a cursor

# cursor = contosodb.cursor()

# ========= Fetch data from the database ===============
@sl.cache_data
def fetch_data():
    data = pd.read_sql_query("select * from factsale limit 50000", contosodb)
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
