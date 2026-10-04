import os
import requests
from supabase import create_client, Client

# 1. Load Environment Variables (Supabase Credentials)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE_NAME = "trending_products"

def fetch_trending_products():
    """
    Simulates fetching high-intent viral products from a trending data source,
    API, or curated list. (Replace this function with your scraper API call 
    or Apify webhook data ingestion when ready).
    """
    print("Fetching latest viral and trending products...")
    
    # Mock data representing trending social commerce items (Dupes & Aesthetic Decor)
    raw_trending_data = [
        {
            "title": "Cloud Couch Aesthetic Dupe (Modular)",
            "category": "Dupes & Home",
            "price": "$450.00",
            "product_url": "https://www.amazon.com/dp/example1",
            "tag": "amazon"
        },
        {
            "title": "Sunset Projection Lamp (16-Color)",
            "category": "Aesthetic Room Decor",
            "price": "$18.99",
            "product_url": "https://www.amazon.com/dp/example2",
            "tag": "amazon"
        },
        {
            "title": "Heateless Curling Rod Headband",
            "category": "Glow-Up & Beauty",
            "price": "$12.50",
            "product_url": "https://www.amazon.com/dp/example3",
            "tag": "amazon"
        },
        {
            "title": "Minimalist Clear Spice Jar Set (24 Pack)",
            "category": "Pantry & Organization",
            "price": "$24.99",
            "product_url": "https://www.amazon.com/dp/example4",
            "tag": "amazon"
        }
    ]
    
    return raw_trending_data

def process_and_insert_data(products):
    """
    Cleans data, injects custom affiliate tracking parameters, 
    and upserts into Supabase.
    """
    success_count = 0
    
    for item in products:
        # Generate or append your custom affiliate tracking tag here
        base_url = item["product_url"]
        affiliate_tag = "?tag=yourstore-20"  # Your Amazon Associates / affiliate tracking ID
        affiliate_url = f"{base_url}{affiliate_tag}"
        
        payload = {
            "title": item["title"],
            "category": item["category"],
            "price": item["price"],
            "product_url": base_url,
            "affiliate_url": affiliate_url
        }
        
        try:
            # Upsert based on the unique 'title' constraint to prevent duplicates
            response = supabase.table(TABLE_NAME).upsert(payload, on_conflict="title").execute()
            print(f"Successfully inserted/updated: {item['title']}")
            success_count += 1
        except Exception as e:
            print(f"Database error for {item['title']}: {e}")
            
    print(f"\nSync complete! Successfully processed {success_count} products into Supabase.")

if __name__ == "__main__":
    trending_items = fetch_trending_products()
    if trending_items:
        process_and_insert_data(trending_items)
