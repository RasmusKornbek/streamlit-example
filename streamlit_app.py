import streamlit as st

# Initialize connection.
conn = st.experimental_connection('snowpark')

# Perform query.
df = conn.query('SELECT * from mytable;', ttl=600)

# Print results.
for row in df.itertuples():
    st.write(f"{row.NAME} has a :{row.PET}:")
