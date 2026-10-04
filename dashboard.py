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

# Custom Styling for Mobile-Optimized Aesthetic & Thumbnails
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
    img {
        border-radius: 8px;
        object-fit: cover;
    }
    </style>
""", unsafe_allow_html=True)

# Profile Header
st.markdown("<h1 style='text-align: center;'>✨ Viral Finds & Dupes</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>As seen on TikTok & IG Reels. Shop my exact aesthetic recommendations below!</p>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar for Admin Control (Allows manual additions/updates including images)
with st.sidebar:
    st.header("⚙️ Store Admin Panel")
    st.subheader("Add or Update Product")
    
    with st.form("admin_form"):
        admin_title = st.text_input("Product Title")
        admin_category = st.selectbox("Category", ["Dupes & Home", "Aesthetic Room Decor", "Glow-Up & Beauty", "Pantry & Organization", "Fashion Staples"])
        admin_price = st.text_input("Price (e.g., $18.99)")
        admin_image_url = st.text_input("Image Thumbnail URL", value="https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300")
        admin_product_url = st.text_input("Original Product URL", value="https://")
        admin_affiliate_url = st.text_input("Affiliate Tracking URL", value="https://")
        
        submitted = st.form_submit_button("Save Product")
        if submitted and admin_title and admin_price:
            try:
                # Check if image_url column exists or insert safely
                payload = {
                    "title": admin_title,
                    "category": admin_category,
                    "price": admin_price,
                    "image_url": admin_image_url,
                    "product_url": admin_product_url,
                    "affiliate_url": admin_affiliate_url
                }
                supabase.table(TABLE_NAME).upsert(payload, on_conflict="title").execute()
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
        
        # Category Filter Selectbox
        categories = ["All"] + list(df["category"].unique())
        selected_category = st.selectbox("Filter by Category:", categories)
        
        if selected_category != "All":
            df = df[df["category"] == selected_category]
            
        st.markdown(f"### 🛍️ Curated Products ({len(df)})")
        
        # Ensure image_url column exists in dataframe to prevent key errors
        if "image_url" not in df.columns:
            df["image_url"] = ""

        # Render as a rich, thumbnail-supported product grid
        for index, row in df.iterrows():
            with st.container():
                col_img, col_info, col_btn = st.columns([1, 2.2, 1.2])
                
                # Column 1: Product Thumbnail Image
                with col_img:
                    img_src = row.get('image_url')
                    if pd.notna(img_src) and str(img_src).startswith("http"):
                        st.image(img_src, use_column_width=True)
                    else:
                        # Fallback icon if no image provided
                        st.markdown("<div style='text-align: center; font-size: 35px; padding-top: 10px;'>📦</div>", unsafe_allow_html=True)
                
                # Column 2: Product Title, Category, & Price
                with col_info:
                    st.markdown(f"**{row.get('title', 'Product')}**")
                    st.caption(f"📂 {row.get('category', 'General')}  \n💰 **{row.get('price', '$0.00')}**")
                
                # Column 3: High-Converting CTA Button
                with col_btn:
                    aff_link = row.get('affiliate_url') or row.get('product_url') or '#'
                    st.markdown(
                        f"""
                        <div style="padding-top: 8px;">
                            <a href="{aff_link}" target="_blank" style="
                                display: block;
                                text-align: center;
                                background-color: #ff3366;
                                color: white;
                                padding: 10px 8px;
                                border-radius: 6px;
                                text-decoration: none;
                                font-weight: bold;
                                font-size: 13px;
                            ">Claim Deal 🔥</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown("---")
                
        # Expandable raw data view for debugging
        with st.expander("🛠️ View Raw Database"):
            st.dataframe(df, use_container_width=True)
            
    else:
        st.warning("No products found in your database yet. Use the sidebar admin panel to add products!")

except Exception as e:
    st.error(f"Error loading products from Supabase: {e}")
