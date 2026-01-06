from jinja2 import Environment, FileSystemLoader
from fetch_news import fetch_news
from dedupe_rank import dedupe_articles, rank_articles
from ai_summary import summarize

env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("newsletter.html")

def build_html():
    raw_articles = fetch_news()
    unique_articles = dedupe_articles(raw_articles)
    top_articles = rank_articles(unique_articles)

    for article in top_articles:
        article["ai_summary"] = summarize(article)

    html = template.render(articles=top_articles)

    with open("newsletter_output.html", "w", encoding="utf-8") as f:
        f.write(html)

    return html


from send_email import send_email
import traceback
import os

def run():
    try:
        print("🚀 Starting newsletter generation...")
        html_content = build_html()

        if os.getenv("NEWS_API_KEY"):
            send_email("📰 Weekly Logistics Newsletter", html_content)
            print("✅ Newsletter generated and sent successfully.")
        else:
            print("⚠️ NEWS_API_KEY missing (using mock data). Skipping email send.")
            print("✅ Newsletter generated locally: newsletter_output.html")

    except Exception as e:
        error_msg = f"❌ Newsletter Generation Failed: {str(e)}"
        print(error_msg)
        print(traceback.format_exc())

if __name__ == "__main__":
    run()
