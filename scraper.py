import os
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client

# 1. Connect to Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Define real AI tool targets to track
AI_TARGETS = [
    {
        "saas_name": "ChatGPT Plus",
        "url": "https://openai.com/chatgpt/pricing/",
        "price_selector": ".pricing-card-price, span[class*='price'], div[class*='price']"
    },
    {
        "saas_name": "Perplexity Pro",
        "url": "https://www.perplexity.ai/pro",
        "price_selector": "div[class*='price'], span[class*='price']"
    },
    {
        "saas_name": "Cursor Pro",
        "url": "https://www.cursor.com",
        "price_selector": ".text-4xl, div[class*='price']"
    }
]

# 3. Scrape and Insert Loop
for target in AI_TARGETS:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        response = requests.get(target["url"], headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Find the price element
            price_element = soup.select_one(target["price_selector"])
            price_text = price_element.get_text(strip=True) if price_element else "Check site"
            
            # Clean up text if it grabs too much junk HTML
            if len(price_text) > 30:
                price_text = "Dynamic / Custom"

            data_to_insert = {
                "title": target["saas_name"],
                "price": price_text,
                "url": target["url"]
            }
            
            # Insert record into Supabase
            supabase.table("prices").insert(data_to_insert).execute()
            print(f"Successfully scraped AI tool: {target['saas_name']} -> {price_text}")
        else:
            print(f"Failed to fetch {target['url']}, status code: {response.status_code}")
            
    except Exception as e:
        print(f"Error processing {target['saas_name']}: {e}")
