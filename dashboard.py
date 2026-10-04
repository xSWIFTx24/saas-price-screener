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

table_name = "prices" 

try:
    # Fetch data
    response = supabase.table(table_name).select("*").execute()
    data = response.data
    
    # If the table is empty, auto-insert a sample row so you see it work instantly!
    if not data:
        supabase.table(table_name).insert({
            "title": "Linear (Sample Tool)",
            "price": "$10/user/mo",
            "url": "https://linear.com/pricing"
        }).execute()
        
        # Re-fetch the data after inserting
        response = supabase.table(table_name).select("*").execute()
        data = response.data

    if data:
        df = pd.DataFrame(data)
        st.success("Successfully connected and loaded data from Supabase!")
        st.metric(label="Total SaaS Tools Tracked", value=len(df))
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Table is currently empty.")

except Exception as e:
    st.error(f"Error connecting to Supabase: {e}")
