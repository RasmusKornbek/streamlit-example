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
    "BusinessUnit",
    "City",
    "Country",
    "EEID",
    "Ethnicity",
    "ExitDate",
    "FullName",
    "Gender",
    "HireDate",
    "JobTitle"
FROM ALTERYXCLOUD.dsi.streamlit_salary
"""

# Execute the query and fetch data into a DataFrame
cursor = conn.cursor()
cursor.execute(sql_query)
data = cursor.fetchall()
df = pd.DataFrame(data, columns=[
    'Salary', 'BusinessUnit', 'City', 'Country', 'EEID', 
    'Ethnicity', 'ExitDate', 'FullName', 'Gender', 'HireDate', 'JobTitle'
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
businessunit=st.sidebar.multiselect(
    "Select Business Unit",
     options=df["BusinessUnit"].unique(),
     default=df["BusinessUnit"].unique(),
)


df_selection=df.query(
    "Country==@country & City==@city & BusinessUnit==@businessunit"
)


def Home():
    with st.expander("⏰ Test"):
        showData=st.multiselect('Filter: ',df_selection.columns,default=['Salary', 'BusinessUnit', 'City', 'Country', 'EEID', 
    'Ethnicity', 'ExitDate', 'FullName', 'Gender', 'HireDate', 'JobTitle'])
        st.dataframe(df_selection[showData],use_container_width=True)
    #compute top analytics
    total_investment = float(df_selection['Salary'].sum())
    investment_mode = float(df_selection['Salary'].mode())
    investment_mean = float(df_selection['Salary'].mean())
    investment_median= float(df_selection['Salary'].median()) 
    rating = float(df_selection['Salary'].sum())


    total1,total2,total3,total4,total5=st.columns(5,gap='large')
    with total1:
        st.info('Total Investment',icon="📌")
        st.metric(label="sum TZS",value=f"{total_investment:,.0f}")

    with total2:
        st.info('Most frequent',icon="📌")
        st.metric(label="mode TZS",value=f"{investment_mode:,.0f}")

    with total3:
        st.info('Average',icon="📌")
        st.metric(label="average TZS",value=f"{investment_mean:,.0f}")

    with total4:
        st.info('Central Earnings',icon="📌")
        st.metric(label="median TZS",value=f"{investment_median:,.0f}")

    with total5:
        st.info('Ratings',icon="📌")
        st.metric(label="Rating",value=numerize(rating),help=f""" Total Rating: {rating} """)

    st.markdown("""---""")



#graphs
def graphs():
    #total_investment=int(df_selection["Investment"]).sum()
    #averageRating=int(round(df_selection["Rating"]).mean(),2)
    
    #simple bar graph
    investment_by_business_type=(
        df_selection.groupby(by=["BusinessUnit"]).count()[["Salary"]].sort_values(by="BusinessUnit")
    )
    fig_investment=px.bar(
       investment_by_business_type,
       x="Salary",
       y=investment_by_business_type.index,
       orientation="h",
       title="<b> Investment by Business Type </b>",
       color_discrete_sequence=["#0083B8"]*len(investment_by_business_type),
       template="plotly_white",
    )


    fig_investment.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
     )


