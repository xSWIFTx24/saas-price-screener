import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

print(f"DEBUG URL value is: '{SUPABASE_URL}'")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Define the target SaaS competitors you want to track
TARGETS = [
    {
        "saas_name": "ExampleTool",
        "url": "https://example.com/pricing",
        # CSS Selectors tailored to the site's HTML structure
        "plan_selector": ".pricing-card-title", 
        "price_selector": ".pricing-card-price"
    }
]

def scrape_pricing_page(target):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(target["url"], headers=headers, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch {target['saas_name']}: Status {response.status_code}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all matching elements on the page
        plans = soup.select(target["plan_selector"])
        prices = soup.select(target["price_selector"])
        
        scraped_data = []
        for plan, price in zip(plans, prices):
            plan_name = plan.get_text(strip=True)
            raw_price = price.get_text(strip=True)
            
            # Clean price string (e.g., "$29/mo" -> 29.0)
            numeric_price = float(''.join(c for c in raw_price if c.isdigit() or c == '.'))
            
            record = {
                "saas_name": target["saas_name"],
                "plan_name": plan_name,
                "price": numeric_price,
                "raw_text": raw_price
            }
            scraped_data.append(record)
            
        return scraped_data

    except Exception as e:
        print(f"Error scraping {target['saas_name']}: {e}")
        return []

def main():
    for target in TARGETS:
        print(f"Scraping {target['saas_name']}...")
        data = scrape_pricing_page(target)
        
        if data:
            for item in data:
                # Upsert into Supabase (updates if exists, inserts if new)
                supabase.table("saas_pricing_tracker").upsert(item).execute()
            print(f"Successfully updated database for {target['saas_name']}")

if __name__ == "__main__":
    main()
