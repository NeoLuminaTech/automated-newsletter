import requests
import os

API_KEY = os.getenv("NEWS_API_KEY")
TOPIC = os.getenv("TOPIC")
URL = f"https://gnews.io/api/v4/search?q={TOPIC}&lang=en&max=10&token={API_KEY}"


def fetch_news():
    if not API_KEY:
        print("⚠️ No NEWS_API_KEY found. Using mock data.")
        return [
            {
                "title": "Mock News: AI takes over the world",
                "description": "In a surprising turn of events, AI has decided to run all newsletters.",
                "url": "https://example.com/ai-news",
                "image": "https://via.placeholder.com/600x300",
                "source": {"name": "Mock Source"}
            },
             {
                "title": "Mock News: Python 4.0 Released",
                "description": "The new version of Python is interpreted by thought alone.",
                "url": "https://example.com/python-news",
                "image": "https://via.placeholder.com/600x300",
                "source": {"name": "Mock Source"}
            }
        ]

    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()
    return data["articles"]

if __name__ == "__main__":
    print(fetch_news())
