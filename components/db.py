import streamlit as sl
import pandas as pd

# ========= Fetch data from CSV instead of SQLite ===============
@sl.cache_data
def fetch_data():
    data = pd.read_csv("WineDataset.csv")  # 读取 CSV 文件
    return data

# 读取数据
data = fetch_data()

# =========== 处理日期数据 ===========
# 如果 CSV 里有 "DateKey" 列，就进行日期处理
if "DateKey" in data.columns:
    data["DateKey"] = pd.to_datetime(data["DateKey"])  # 转换为日期格式
    data["Year"] = data["DateKey"].dt.year  # 提取年份
    data["Month"] = data["DateKey"].dt.month_name()  # 提取月份（英文）
    data["Month_Number"] = data["DateKey"].dt.month  # 提取月份（数字）
    data["Day_Name"] = data["DateKey"].dt.day_name()  # 提取星期几
    data["Day_Number"] = data["DateKey"].dt.day  # 提取日期（数字）

# 显示数据（可选）
sl.write(data.head())  # 在 Streamlit 界面显示前 5 行数据
