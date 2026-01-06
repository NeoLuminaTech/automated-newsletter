import requests
import os
import time
from config import LANGUAGE, validate_config

# Ensure config is valid before proceeding (this runs at import time or first call)
# Better to call validate_config() inside the function or main execution to control when it fails.

def fetch_news():
    """
    Fetches news articles from GNews API.
    Raises exceptions on failure. No mock data.
    """
    API_KEY = os.getenv("NEWS_API_KEY")
    if not API_KEY:
        raise EnvironmentError("NEWS_API_KEY is missing from environment variables.")

    QUERY = os.getenv("SEARCH_QUERY") or (
        "Supply Chain OR Logistics OR Freight OR Cargo OR Warehouse "
        "OR Sustainability OR Green Logistics OR Logistics Technology"
    )

    URL = (
        "https://gnews.io/api/v4/search"
        f"?q={QUERY}&lang={LANGUAGE}&max=20&token={API_KEY}"
    )

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (NewsletterBot/1.0)"
    }

    print(f"🌍 Fetching news for query: '{QUERY}'...")

    for attempt in range(3):
        try:
            response = requests.get(URL, headers=HEADERS, timeout=10)
            response.raise_for_status()
            articles = response.json().get("articles", [])
            
            if not articles:
                 print("⚠️ API returned 0 articles.")
                 # Decide if 0 articles is an error. 
                 # For a newsletter system, 0 articles might be valid but rare. 
                 # However, usually we want to know if the search is broken.
                 # Let's return empty list but NOT mock.
                 return []
            
            print(f"✅ Fetched {len(articles)} articles.")
            return articles

        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print(f"⏳ Rate limited (Attempt {attempt+1}/3). Sleeping 10s...")
                time.sleep(10)
            else:
                # Re-raise non-retriable HTTP errors immediately
                raise RuntimeError(f"News API HTTP Error: {e}") from e
        except requests.exceptions.RequestException as e:
            # Network errors, timeouts, etc.
            if attempt == 2:
               raise RuntimeError(f"News API Network Error after 3 attempts: {e}") from e
            print(f"⚠️ Network error (Attempt {attempt+1}/3): {e}")
            time.sleep(2)
    
    raise RuntimeError("Failed to fetch news after max retries.")

if __name__ == "__main__":
    try:
        articles = fetch_news()
        print(f"Fetched {len(articles)} articles")
    except Exception as e:
        print(f"❌ Test Failed: {e}")
