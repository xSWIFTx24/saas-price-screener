import os
from supabase import create_client
import streamlit as st
import pandas as pd

st.set_page_config(page_title="SaaS Price Screener", layout="wide")

# Connect to Supabase using environment variables (or Streamlit Secrets)
url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")
supabase = create_client(url, key)

st.title("🚀 Live SaaS Price Screener")

# Fetch data from your Supabase table 
# (Replace "your_table_name" with the actual name of your table in Supabase)
try:
    response = supabase.table("your_table_name").select("*").execute()
    data = response.data
    
    if data:
        df = pd.DataFrame(data)
        
        # Display metrics or your main data table
        st.metric(label="Total Tracked Items", value=len(df))
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Connected to Supabase successfully, but the table is currently empty. Run your GitHub Action to scrape some data!")

except Exception as e:
    st.error(f"Error connecting to Supabase: {e}")

# 3. Create high-level metrics
st.subheader("At a Glance")
col1, col2, col3 = st.columns(3)

# Display the top performer
top_trend = df.loc[df['Daily Views'].idxmax()]
col1.metric("Top Trend", top_trend['Trend Topic'], f"{top_trend['Weekly Growth (%)']}%")

# Display fastest growing
fastest = df.loc[df['Weekly Growth (%)'].idxmax()]
col2.metric("Fastest Growing", fastest['Trend Topic'], f"{fastest['Weekly Growth (%)']}%")

# Display total tracked views
total_views = df['Daily Views'].sum()
col3.metric("Total Tracked Views", f"{total_views / 1000000:.1f}M")

st.divider()

# 4. Interactive visualizations and filters
col_chart, col_data = st.columns([2, 1])

with col_chart:
    st.subheader("Views by Trend")
    # Streamlit natively supports bar, line, and area charts
    st.bar_chart(df, x="Trend Topic", y="Daily Views", color="#FF4B4B")

with col_data:
    st.subheader("Filter Data")
    # Add an interactive dropdown filter
    platform = st.selectbox("Select Platform", ["All"] + list(df['Platform'].unique()))
    
    if platform != "All":
        filtered_df = df[df['Platform'] == platform]
    else:
        filtered_df = df
        
    st.dataframe(filtered_df[['Trend Topic', 'Daily Views']], hide_index=True)
