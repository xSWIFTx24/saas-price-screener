import streamlit as st
import pandas as pd

# 1. Configure the page
st.set_page_config(page_title="Social Trends", page_icon="📈", layout="wide")

st.title("📈 Daily Social Media Trends")
st.markdown("Tracking top performing fashion Shorts across platforms.")

# 2. Load mock data (In production, this would be a database query)
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Trend Topic": ["#OOTD", "#Y2K", "#Streetwear", "#Vintage", "#Thrifting"],
        "Daily Views": [1500000, 940000, 850000, 620000, 310000],
        "Weekly Growth (%)": [12, 18, 5, -2, 4],
        "Platform": ["TikTok", "YouTube", "TikTok", "Instagram", "YouTube"]
    })

df = load_data()

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
