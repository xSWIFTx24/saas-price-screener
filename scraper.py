import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client

# 1. Connect to Supabase using environment variables
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Define the target SaaS competitors you want to track
TARGETS = [
    {
        "saas_name": "ExampleTool",
        "url": "https://example.com/pricing",
        # CSS Selectors tailored to the site's HTML structure
        "price_selector": ".pricing-card-price"
    }
]

# 3. Scrape and Insert Loop
for target in TARGETS:
    try:
        # Add a basic user-agent header so websites don't block the request
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        response = requests.get(target["url"], headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find the price element using the CSS selector
            price_element = soup.select_one(target["price_selector"])
            price_text = price_element.get_text(strip=True) if price_element else "Price not found"
            
            # Prepare data mapping to match your Supabase table columns: title, price, url
            data_to_insert = {
                "title": target["saas_name"],
                "price": price_text,
                "url": target["url"]
            }
            
            # Insert the record into Supabase
            supabase.table("prices").insert(data_to_insert).execute()
            print(f"Successfully scraped and saved: {target['saas_name']} -> {price_text}")
        else:
            print(f"Failed to fetch {target['url']}, status code: {response.status_code}")
            
    except Exception as e:
        print(f"Error processing {target['saas_name']}: {e}")
