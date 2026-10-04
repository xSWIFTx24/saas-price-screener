import os
from supabase import create_client
import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="SaaS Price Screener", layout="wide")

st.title("🚀 SaaS Price Tracking Dashboard")

# 1. Connect to Supabase
try:
    url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")
    
    if not url or not key:
        st.error("Missing Supabase credentials in Streamlit Secrets!")
        st.stop()
        
    supabase = create_client(url, key)
except Exception as e:
    st.error(f"Failed to initialize Supabase: {e}")
    st.stop()

# 2. Fetch data from the 'prices' table we just created
table_name = "prices" 

try:
    response = supabase.table(table_name).select("*").execute()
    data = response.data
    
    if data:
        df = pd.DataFrame(data)
        
        # Display top metrics
        st.metric(label="Total SaaS Tools Tracked", value=len(df))
        
        # Display the interactive data table
        st.subheader("Latest Scraped Pricing Data")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning(f"Your table '{table_name}' is currently connected, but it's empty! Head over to GitHub and trigger your scraper action to pull in some SaaS prices.")

except Exception as e:
    st.error(f"Error fetching data from table '{table_name}': {e}")
