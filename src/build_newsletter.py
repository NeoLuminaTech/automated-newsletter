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

# ... (rest of imports are fine, checks below)

def run():
    try:
        print("🚀 Starting newsletter generation...")
        html_content = build_html()
        send_email("📰 Weekly Logistics Newsletter", html_content)
        print("✅ Newsletter generated and sent successfully.")
    except Exception as e:
        error_msg = f"❌ Newsletter Generation Failed: {str(e)}"
        print(error_msg)
        trace = traceback.format_exc()
        send_email(
            "⚠️ Newsletter Generation Failed",
            f"<h1>Generation Failed</h1><p>{error_msg}</p><pre>{trace}</pre>"
        )

if __name__ == "__main__":
    run()
