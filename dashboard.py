import os
from supabase import create_client
import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="SaaS Price Screener", layout="wide")
st.title("🚀 SaaS Price Tracking Dashboard")

# 1. Connect to Supabase
url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")
supabase = create_client(url, key)

# 2. Fetch data from the 'prices' table
table_name = "prices" 

try:
    response = supabase.table(table_name).select("*").execute()
    
    # DEBUG: Print raw response to the dashboard screen so we can see it
    st.write("Raw Supabase Response:", response)
    
    data = response.data
    
    if data:
        df = pd.DataFrame(data)
        st.metric(label="Total SaaS Tools Tracked", value=len(df))
        st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"Table '{table_name}' returned 0 rows.")

except Exception as e:
    st.error(f"Error fetching data: {e}")
