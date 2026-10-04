import os
from playwright.sync_api import sync_playwright
from supabase import create_client, Client

# 1. Connect to Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 2. Define AI targets with custom affiliate links and selectors
AI_TARGETS = [
    {
        "saas_name": "ChatGPT Plus",
        "url": "https://openai.com/chatgpt/pricing/",
        "affiliate_url": "https://openai.com/chatgpt",
        "price_selector": "text=$"  # Finds text containing a dollar sign
    },
    {
        "saas_name": "Perplexity Pro",
        "url": "https://www.perplexity.ai/pro",
        "affiliate_url": "https://www.perplexity.ai/pro?ref=your_affiliate_code",
        "price_selector": "text=$"
    },
    {
        "saas_name": "Cursor Pro",
        "url": "https://www.cursor.com",
        "affiliate_url": "https://www.cursor.com?ref=your_affiliate_code",
        "price_selector": "text=$"
    }
]

# 3. Run Playwright Scraper
with sync_playwright() as p:
    # Launch headless browser
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for target in AI_TARGETS:
        try:
            print(f"Navigating to {target['saas_name']}...")
            # Go to page and wait until network is idle (ensures JS finishes loading)
            page.goto(target["url"], timeout=40000, wait_until="networkidle")
            
            # Try to locate the price element
            price_text = "Check site"
            try:
                # Look for elements containing pricing structures or dollar signs
                price_element = page.locator(target["price_selector"]).first
                if price_element.is_visible():
                    extracted = price_element.inner_text().strip()
                    # Clean up if it grabbed too much surrounding text block
                    if len(extracted) < 20 and "$" in extracted:
                        price_text = extracted
            except Exception:
                pass

            # Prepare data mapping including your affiliate link
            data_to_insert = {
                "title": target["saas_name"],
                "price": price_text,
                "url": target["url"],
                "affiliate_url": target["affiliate_url"]
            }
            
            # Insert into Supabase
            supabase.table("prices").insert(data_to_insert).execute()
            print(f"Successfully scraped & saved: {target['saas_name']} -> {price_text}")

        except Exception as e:
            print(f"Error processing {target['saas_name']}: {e})

    browser.close()
