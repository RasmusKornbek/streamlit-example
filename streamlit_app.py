import streamlit as st
import snowflake.connector
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
#from query import *
import time

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
st.subheader("🔔  Analytics Dashboard")
st.markdown("##")

theme_plotly = None # None or streamlit


#Connect to Snowflake
# Get Snowflake secrets from Streamlit Secrets
snowflake_account = st.secrets["account"]
snowflake_username = st.secrets["username"]
snowflake_password = st.secrets["password"]
snowflake_database = st.secrets["database"]
snowflake_role = st.secrets["role"]
snowflake_schema = st.secrets["schema"]

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=snowflake_account,
    user=snowflake_username,
    password=snowflake_password,
    database=snowflake_database,
    role=snowflake_role,
    schema=snowflake_schema
)

# SQL query
sql_query = """
SELECT 
    Salary,
    "Business Unit",
    "City",
    "Country",
    "EEID",
    "Ethnicity",
    "Exit Date",
    "Full Name",
    "Gender",
    "Hire Date",
    "Job Title"
FROM ALTERYXCLOUD.dsi.streamlit_salary
"""

# Execute the query and fetch data into a DataFrame
cursor = conn.cursor()
cursor.execute(sql_query)
data = cursor.fetchall()
df = pd.DataFrame(data, columns=[
    'Salary', 'Business Unit', 'City', 'Country', 'EEID', 
    'Ethnicity', 'Exit Date', 'Full Name', 'Gender', 'Hire Date', 'Job Title'
])

# Close the cursor and connection
cursor.close()
conn.close()
 


#side bar
st.sidebar.image("logo1.png",caption="Developed and Maintaned by: Rasmus: +4528765537")


#switcher
st.sidebar.header("Please filter")
country=st.sidebar.multiselect(
    "Select Country",
     options=df["Country"].unique(),
     default=df["Country"].unique(),
)
city=st.sidebar.multiselect(
    "Select City",
     options=df["City"].unique(),
     default=df["City"].unique(),
)
BU=st.sidebar.multiselect(
    "Select Business Unit",
     options=df["Business Unit"].unique(),
     default=df["Business Unit"].unique(),
)


df_selection=df.query(
    "Country==@country & City==@city & `Business Unit`==@BU"
)

def Home():
    with st.expander("⏰ My Excel WorkBook"):
        showData=st.multiselect('Filter: ',df_selection.columns,default=['Salary', 'Business Unit', 'City', 'Country', 'EEID', 
    'Ethnicity', 'Exit Date', 'Full Name', 'Gender', 'Hire Date', 'Job Title'])
        st.dataframe(df_selection[showData],use_container_width=True)
    #compute top analytics
    total_investment = float(df_selection['Salary'].sum())
    investment_mode = float(df_selection['Salary'].mode())
    investment_mean = float(df_selection['Salary'].mean())
    investment_median= float(df_selection['Salary'].median()) 
    rating = float(df_selection['Salary'].sum())

