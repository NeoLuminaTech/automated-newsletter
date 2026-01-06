import requests
import os
from config import TOPICS, LANGUAGE, MAX_ARTICLES_PER_TOPIC

API_KEY = os.getenv("NEWS_API_KEY")

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

    all_articles = []

    for topic in TOPICS:
        url = (
            "https://gnews.io/api/v4/search"
            f"?q={topic}&lang={LANGUAGE}"
            f"&max={MAX_ARTICLES_PER_TOPIC}&token={API_KEY}"
        )

        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        all_articles.extend(data.get("articles", []))

    return all_articles

if __name__ == "__main__":
    print(len(fetch_news()))
