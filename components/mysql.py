import mysql.connector as cn
import streamlit as sl

# ====================Connect to the Database============
contosodb = cn.connect(
    host='localhost',
    user='root',
    password='ekedie',
    database='contoso_store'
)

# create a cursor

cursor = contosodb.cursor()