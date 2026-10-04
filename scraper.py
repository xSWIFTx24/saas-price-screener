import os
from supabase import create_client, Client
from trendspyg import download_google_trends_rss

# 1. Load Environment Variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
TABLE_NAME = "trending_products"

def fetch_live_google_trends():
    """
    Pulls real-time trending searches from Google Trends RSS feed 
    using trendspyg, mapping live search momentum into product ideas.
    """
    print("Fetching live trending data from Google Trends...")
    dynamic_products = []
    
    try:
        # Fetch real-time US trending searches snapshot
        trend_data = download_google_trends_rss(geo='US', normalize=True)
        items = trend_data.get('trends', [])
        
        for item in items[:10]: # Grab top 10 breaking trends
            keyword = item.get('keyword')
            # Format into a product-like entry matching your Supabase table
            dynamic_products.append({
                "title": f"Trending: {keyword.title()} Find",
                "category": "Viral Live Trends",
                "price": "$19.99", # Default placeholder price for live trends
                "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300",
                "product_url": f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}"
            })
    except Exception as e:
        print(f"Warning: Could not fetch live RSS trends ({e}). Falling back to curated catalog.")
        
    return dynamic_products

def get_core_catalog():
    """Your core high-converting evergreen dupe and aesthetic catalog."""
    return [
        {
            "title": "Cloud Couch Aesthetic Modular Dupe",
            "category": "Dupes & Home",
            "price": "$450.00",
            "image_url": "https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=300",
            "product_url": "https://www.amazon.com/dp/B08X5XYZ1"
        },
        {
            "title": "16-Color Sunset Projection Lamp",
            "category": "Aesthetic Room Decor",
            "price": "$18.99",
            "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300",
            "product_url": "https://www.amazon.com/dp/B07Z5XYZ6"
        },
        {
            "title": "Heateless Curling Rod Headband Kit",
            "category": "Glow-Up & Beauty",
            "price": "$12.50",
            "image_url": "https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=300",
            "product_url": "https://www.amazon.com/dp/B07Y5XYZ11"
        },
        {
            "title": "Viral Seamless Butter-Soft Workout Set",
            "category": "Fashion Staples",
            "price": "$34.99",
            "image_url": "https://images.unsplash.com/photo-1517838277536-f5f99be501cd?w=300",
            "product_url": "https://www.amazon.com/dp/B07V5XYZ21"
        }
    ]

def process_and_sync():
    # Combine live breaking search trends with your high-converting core items
    live_trends = fetch_live_google_trends()
    core_items = get_core_catalog()
    all_products = live_trends + core_items
    
    success_count = 0
    for item in all_products:
        base_url = item["product_url"]
        # Affiliate tracking tag insertion
        affiliate_tag = "?tag=yourstore-20"
        affiliate_url = base_url if "?" in base_url else f"{base_url}{affiliate_tag}"
        
        payload = {
            "title": item["title"],
            "category": item["category"],
            "price": item["price"],
            "image_url": item.get("image_url", ""),
            "product_url": base_url,
            "affiliate_url": affiliate_url
        }
        
        try:
            supabase.table(TABLE_NAME).upsert(payload, on_conflict="title").execute()
            print(f"Synced: {item['title']}")
            success_count += 1
        except Exception as e:
            print(f"Error syncing {item['title']}: {e}")
            
    print(f"\nSync complete! Successfully processed {success_count} products into Supabase.")

if __name__ == "__main__":
    process_and_sync()
