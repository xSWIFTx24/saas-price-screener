import os
from supabase import create_client
import streamlit as st
import pandas as pd

# Page Configuration for Mobile-First Link-in-Bio Vibe
st.set_page_config(
    page_title="Viral Finds & Aesthetic Dupes", 
    page_icon="✨", 
    layout="centered"
)

# 1. Connect to Supabase
url = os.environ.get("SUPABASE_URL") or st.secrets.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY") or st.secrets.get("SUPABASE_KEY")
supabase = create_client(url, key)

TABLE_NAME = "trending_products"

# Custom Styling for Mobile-Optimized Aesthetic
st.markdown("""
    <style>
    .main {
        max-width: 600px;
        margin: 0 auto;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Profile Header
st.markdown("<h1 style='text-align: center;'>✨ Viral Finds & Dupes</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>As seen on TikTok & IG Reels. Shop my exact aesthetic recommendations below!</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar for Admin Control (Allows manual additions/updates)
with st.sidebar:
    st.header("⚙️ Store Admin Panel")
    st.subheader("Add or Update Product")
    
    with st.form("admin_form"):
        admin_title = st.text_input("Product Title")
        admin_category = st.selectbox("Category", ["Dupes & Home", "Aesthetic Room Decor", "Glow-Up & Beauty", "Pantry & Organization", "Fashion Staples"])
        admin_price = st.text_input("Price (e.g., $18.99)")
        admin_product_url = st.text_input("Original Product URL", value="https://")
        admin_affiliate_url = st.text_input("Affiliate Tracking URL", value="https://")
        
        submitted = st.form_submit_button("Save Product")
        if submitted and admin_title and admin_price:
            try:
                supabase.table(TABLE_NAME).upsert({
                    "title": admin_title,
                    "category": admin_category,
                    "price": admin_price,
                    "product_url": admin_product_url,
                    "affiliate_url": admin_affiliate_url
                }, on_conflict="title").execute()
                st.success(f"Successfully saved {admin_title}!")
                st.rerun()
            except Exception as e:
                st.error(f"Error saving: {e}")

# Fetch data from Supabase
try:
    response = supabase.table(TABLE_NAME).select("*").execute()
    data = response.data
    
    if data:
        df = pd.DataFrame(data)
        
        # Category Filter Pills / Selectbox
        categories = ["All"] + list(df["category"].unique())
        selected_category = st.selectbox("Filter by Category:", categories)
        
        if selected_category != "All":
            df = df[df["category"] == selected_category]
            
        st.markdown(f"### 🛍️ Curated Products ({len(df)})")
        
        # Render as clean, high-converting product rows/cards
        for index, row in df.iterrows():
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**{row.get('title', 'Product')}**")
                    st.caption(f"📂 {row.get('category', 'General')} | 💰 **{row.get('price', '$0.00')}**")
                
                with col2:
                    aff_link = row.get('affiliate_url') or row.get('product_url') or '#'
                    # High-converting CTA button styling matching social commerce vibes
                    st.markdown(
                        f"""
                        <a href="{aff_link}" target="_blank" style="
                            display: block;
                            text-align: center;
                            background-color: #ff3366;
                            color: white;
                            padding: 8px 12px;
                            border-radius: 6px;
                            text-decoration: none;
                            font-weight: bold;
                            font-size: 14px;
                            margin-top: 5px;
                        ">Claim Deal 🔥</a>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown("---")
                
        # Expandable raw data view for debugging / admin management
        with st.expander("🛠️ View Raw Database"):
            st.dataframe(df, use_container_width=True)
            
    else:
        st.warning("No products found in your database yet. Use the sidebar admin panel to add your first product or run your trend importer script!")

except Exception as e:
    st.error(f"Error loading products from Supabase: {e}")
