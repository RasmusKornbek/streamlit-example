import streamlit as st
import pandas as pd
import snowflake.connector
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pyodbc

# Streamlit app title
st.title("Snowflake Table Viewer")

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


# Assuming you have a valid database connection 'conn'

# SQL query
sql_query = """
SELECT 
    "Salary",
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

# Dashboard layout
st.title('Employee Salary Dashboard')

# Display DataFrame
st.write('## Employee Salary Data')
st.write(df)

# Bar chart of average salary by business unit
st.write('## Average Salary by Business Unit')
avg_salary_by_business_unit = df.groupby('Business Unit')['Salary'].mean()
fig_avg_salary_by_business_unit, ax_avg_salary_by_business_unit = plt.subplots()
ax_avg_salary_by_business_unit.bar(avg_salary_by_business_unit.index, avg_salary_by_business_unit.values)
ax_avg_salary_by_business_unit.set_xlabel('Business Unit')
ax_avg_salary_by_business_unit.set_ylabel('Average Salary')
st.pyplot(fig_avg_salary_by_business_unit)

# Pie chart of salary distribution by gender
st.write('## Salary Distribution by Gender')
salary_distribution_by_gender = df.groupby('Gender')['Salary'].sum()
fig_salary_distribution_by_gender, ax_salary_distribution_by_gender = plt.subplots()
ax_salary_distribution_by_gender.pie(salary_distribution_by_gender, labels=salary_distribution_by_gender.index, autopct='%1.1f%%')
ax_salary_distribution_by_gender.set_aspect('equal')
st.pyplot(fig_salary_distribution_by_gender)
