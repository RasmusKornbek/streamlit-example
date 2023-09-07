import streamlit as st
import pandas as pd
import snowflake.connector

# Streamlit app title
st.title("Snowflake Table Viewer")

# Get Snowflake secrets from Streamlit Secrets
snowflake_account = st.secrets["account"]
snowflake_username = st.secrets["username"]
snowflake_password = st.secrets["password"]
snowflake_database = st.secrets["database"]
snowflake_schema = st.secrets["schema"]
snowflake_table = st.secrets["table"]

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=snowflake_account,
    user=snowflake_username,
    password=snowflake_password,
    database=snowflake_database,
    schema=snowflake_schema
)

# Query Snowflake table
query = f"SELECT * FROM {mytable}"
df = pd.read_sql(query, conn)

# Display the table in Streamlit
st.write(df)

# Close Snowflake connection
conn.close()
