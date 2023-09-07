import streamlit as st
import pandas as pd
import snowflake.connector

# Streamlit app title
st.title("Snowflake Table Viewer")

# Get Snowflake secrets from Streamlit Secrets
snowflake_account = st.secrets["snowflake_account"]
snowflake_username = st.secrets["snowflake_username"]
snowflake_password = st.secrets["snowflake_password"]
snowflake_database = st.secrets["snowflake_database"]
snowflake_schema = st.secrets["snowflake_schema"]
snowflake_table = st.secrets["snowflake_table"]

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=snowflake_account,
    user=snowflake_username,
    password=snowflake_password,
    database=snowflake_database,
    schema=snowflake_schema
)

# Query Snowflake table
query = f"SELECT * FROM {snowflake_table}"
df = pd.read_sql(query, conn)

# Display the table in Streamlit
st.write(df)

# Close Snowflake connection
conn.close()
