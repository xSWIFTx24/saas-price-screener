import os
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
    Curated list of 25 viral short-form video products across 
    Dupes, Aesthetic Decor, Glow-Up, Organization, and Fashion Staples.
    """
    print("Preparing 25 trending products for sync...")
    
    products = [
        # --- Dupes & Home ---
        {
            "title": "Cloud Couch Aesthetic Modular Dupe",
            "category": "Dupes & Home",
            "price": "$450.00",
            "product_url": "https://www.amazon.com/dp/B08X5XYZ1"
        },
        {
            "title": "Skims Ribbed Long Dress Dupe",
            "category": "Dupes & Home",
            "price": "$28.00",
            "product_url": "https://www.amazon.com/dp/B09X5XYZ2"
        },
        {
            "title": "Mason Pearson Hairbrush Viral Dupe",
            "category": "Dupes & Home",
            "price": "$16.99",
            "product_url": "https://www.amazon.com/dp/B07X5XYZ3"
        },
        {
            "title": "Bala Bangles Wrist/Ankle Weight Dupe",
            "category": "Dupes & Home",
            "price": "$19.50",
            "product_url": "https://www.amazon.com/dp/B08X5XYZ4"
        },
        {
            "title": "Brumate Era Insulated Tumbler Dupe",
            "category": "Dupes & Home",
            "price": "$22.99",
            "product_url": "https://www.amazon.com/dp/B0AX5XYZ5"
        },

        # --- Aesthetic Room Decor ---
        {
            "title": "16-Color Sunset Projection Lamp",
            "category": "Aesthetic Room Decor",
            "price": "$18.99",
            "product_url": "https://www.amazon.com/dp/B07Z5XYZ6"
        },
        {
            "title": "Smart LED RGB Strip Lights (Works with Alexa)",
            "category": "Aesthetic Room Decor",
            "price": "$24.99",
            "product_url": "https://www.amazon.com/dp/B08Z5XYZ7"
        },
        {
            "title": "Minimalist Wooden Sunrise Alarm Clock",
            "category": "Aesthetic Room Decor",
            "price": "$35.00",
            "product_url": "https://www.amazon.com/dp/B09Z5XYZ8"
        },
        {
            "title": "Floating Acrylic Invisible Bookshelves (4 Pack)",
            "category": "Aesthetic Room Decor",
            "price": "$21.99",
            "product_url": "https://www.amazon.com/dp/B07Z5XYZ9"
        },
        {
            "title": "Aesthetic Glass Mushroom Table Lamp",
            "category": "Aesthetic Room Decor",
            "price": "$39.99",
            "product_url": "https://www.amazon.com/dp/B08Z5XYZ10"
        },

        # --- Glow-Up & Beauty ---
        {
            "title": "Heatless Curling Rod Headband Kit",
            "category": "Glow-Up & Beauty",
            "price": "$12.50",
            "product_url": "https://www.amazon.com/dp/B07Y5XYZ11"
        },
        {
            "title": "Ice Roller for Face & Eye Puffiness",
            "category": "Glow-Up & Beauty",
            "price": "$14.99",
            "product_url": "https://www.amazon.com/dp/B08Y5XYZ12"
        },
        {
            "title": "Electric Scalp Massager Shampoo Brush",
            "category": "Glow-Up & Beauty",
            "price": "$9.99",
            "product_url": "https://www.amazon.com/dp/B09Y5XYZ13"
        },
        {
            "title": "Rose Quartz Gua Sha & Facial Roller Set",
            "category": "Glow-Up & Beauty",
            "price": "$11.99",
            "product_url": "https://www.amazon.com/dp/B07Y5XYZ14"
        },
        {
            "title": "Portable Mini Makeup Fridge with LED Mirror",
            "category": "Glow-Up & Beauty",
            "price": "$45.00",
            "product_url": "https://www.amazon.com/dp/B08Y5XYZ15"
        },

        # --- Pantry & Organization ---
        {
            "title": "Minimalist Clear Glass Spice Jars (24 Pack)",
            "category": "Pantry & Organization",
            "price": "$24.99",
            "product_url": "https://www.amazon.com/dp/B07W5XYZ16"
        },
        {
            "title": "Aesthetic Clear Fridge & Freezer Bins (6 Pack)",
            "category": "Pantry & Organization",
            "price": "$32.99",
            "product_url": "https://www.amazon.com/dp/B08W5XYZ17"
        },
        {
            "title": "Automatic Soap Dispenser for Kitchen/Bath",
            "category": "Pantry & Organization",
            "price": "$19.99",
            "product_url": "https://www.amazon.com/dp/B09W5XYZ18"
        },
        {
            "title": "Under-Sink Sliding 2-Tier Storage Organizer",
            "category": "Pantry & Organization",
            "price": "$26.50",
            "product_url": "https://www.amazon.com/dp/B07W5XYZ19"
        },
        {
            "title": "Lazy Susan Rotating Pantry Organizer Bins",
            "category": "Pantry & Organization",
            "price": "$21.00",
            "product_url": "https://www.amazon.com/dp/B08W5XYZ20"
        },

        # --- Fashion Staples ---
        {
            "title": "Viral Seamless Butter-Soft Workout Set",
            "category": "Fashion Staples",
            "price": "$34.99",
            "product_url": "https://www.amazon.com/dp/B07V5XYZ21"
        },
        {
            "title": "Oversized Heavyweight Aesthetic Hoodie",
            "category": "Fashion Staples",
            "price": "$38.00",
            "product_url": "https://www.amazon.com/dp/B08V5XYZ22"
        },
        {
            "title": "Minimalist Claw Clips for Thick Hair (8 Pack)",
            "category": "Fashion Staples",
            "price": "$11.99",
            "product_url": "https://www.amazon.com/dp/B09V5XYZ23"
        },
        {
            "title": "Waterproof Gold Chunky Hoop Earrings",
            "category": "Fashion Staples",
            "price": "$14.50",
            "product_url": "https://www.amazon.com/dp/B07V5XYZ24"
        },
        {
            "title": "Quilted Puffer Crossbody Cloud Bag",
            "category": "Fashion Staples",
            "price": "$25.99",
            "product_url": "https://www.amazon.com/dp/B08V5XYZ25"
        }
    ]
    
    return products

def process_and_insert_data(products):
    success_count = 0
    
    for item in products:
        # Append your Amazon Associates tracking tag (update tag=yourstore-20 to your actual ID)
        base_url = item["product_url"]
        affiliate_tag = "?tag=yourstore-20"
        affiliate_url = f"{base_url}{affiliate_tag}"
        
        payload = {
            "title": item["title"],
            "category": item["category"],
            "price": item["price"],
            "product_url": base_url,
            "affiliate_url": affiliate_url
        }
        
        try:
            supabase.table(TABLE_NAME).upsert(payload, on_conflict="title").execute()
            print(f"Synced: {item['title']}")
            success_count += 1
        except Exception as e:
            print(f"Error syncing {item['title']}: {e}")
            
    print(f"\nSync complete! Successfully loaded {success_count} of {len(products)} products into Supabase.")

if __name__ == "__main__":
    items = fetch_trending_products()
    if items:
        process_and_insert_data(items)
