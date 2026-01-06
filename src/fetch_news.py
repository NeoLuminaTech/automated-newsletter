import requests
import os
import time
from config import LANGUAGE

API_KEY = os.getenv("NEWS_API_KEY")
QUERY = os.getenv("SEARCH_QUERY") or (
    "Supply Chain OR Logistics OR Freight OR Cargo OR Warehouse "
    "OR Sustainability OR Green Logistics OR Logistics Technology"
)

def fetch_news():
    if not API_KEY:
        print("⚠️ No NEWS_API_KEY found. Using mock data.")
        return [
            {
                "title": "Mock News: Supply Chain AI Revolution",
                "description": "AI is transforming logistics with predictive analytics.",
                "url": "https://example.com/ai-logistics",
                "image": "https://via.placeholder.com/600x300",
                "source": {"name": "Tech Logistics Daily"}
            },
            {
                "title": "Mock News: Green Freight Initiatives",
                "description": "New regulations push for carbon-neutral shipping.",
                "url": "https://example.com/green-freight",
                "image": "https://via.placeholder.com/600x300",
                "source": {"name": "EcoTransport"}
            },
             {
                "title": "Mock News: Warehouse Robotics",
                "description": "Robots are taking over picking and packing.",
                "url": "https://example.com/warehouse-bots",
                "image": "https://via.placeholder.com/600x300",
                "source": {"name": "AutoWarehouse"}
            }
        ]

    URL = (
        "https://gnews.io/api/v4/search"
        f"?q={QUERY}&lang={LANGUAGE}&max=20&token={API_KEY}"
    )

    HEADERS = {
        "User-Agent": "Mozilla/5.0 (NewsletterBot/1.0)"
    }

    for attempt in range(3):
        try:
            response = requests.get(URL, headers=HEADERS, timeout=10)
            response.raise_for_status()
            return response.json().get("articles", [])
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                print("Rate limited. Sleeping before retry...")
                time.sleep(10 * (attempt + 1))
            else:
                print(f"Error fetching news: {e}")
                return []
        except Exception as e:
            print(f"Unexpected error: {e}")
            return []
    
    return []

if __name__ == "__main__":
    print(len(fetch_news()))
