import requests
import os

API_KEY = os.getenv("NEWS_API_KEY")
TOPIC = "artificial intelligence"
URL = f"https://gnews.io/api/v4/search?q={TOPIC}&lang=en&max=10&token={API_KEY}"

def fetch_news():
    response = requests.get(URL)
    response.raise_for_status()
    data = response.json()
    return data["articles"]

if __name__ == "__main__":
    print(fetch_news())
