from jinja2 import Environment, FileSystemLoader
from fetch_news import fetch_news
from dedupe_rank import dedupe_articles, rank_articles
from ai_summary import summarize
from send_email import send_email, notify_failure
from config import validate_config
import traceback
import os

# Initialize Jinja2 environment (can fail if templates missing, handled in main loop)
try:
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("newsletter.html")
except Exception as e:
    # If this fails at import/init time, we can't do much in the loop, 
    # but strictly speaking this should be inside the run loop for consistent handling,
    # or validated at start. For now, let's leave it global but wrap usage.
    print(f"Template loading warning: {e}")

def build_html():
    """
    Orchestrates the data gathering and HTML generation.
    Raises exceptions on failure.
    """
    # 1. Fetch
    print("Step 1: Fetching News...")
    raw_articles = fetch_news()
    
    # 2. Dedupe & Rank (Local logic, less likely to fail but good to track)
    print("Step 2: Processing Articles...")
    unique_articles = dedupe_articles(raw_articles)
    top_articles = rank_articles(unique_articles)

    if not top_articles:
        raise RuntimeError("No articles remained after deduplication and ranking.")

    # 3. Summarize (DISABLED per user request)
    # print("Step 3: Generating AI Summaries...")
    # for article in top_articles:
    #     # Failure here stops the pipeline (Fail-Fast)
    #     article["ai_summary"] = summarize(article)

    # 4. Render
    print("Step 4: Rendering HTML...")
    html = template.render(articles=top_articles)

    with open("newsletter_output.html", "w", encoding="utf-8") as f:
        f.write(html)

    return html

def run():
    current_stage = "Initialization"
    try:
        print("🚀 Starting newsletter generation pipeline...")
        
        # 0. Validation
        current_stage = "Configuration Validation"
        validate_config()

        # 1-4. Build
        current_stage = "Content Generation (Fetch/Summarize/Render)"
        html_content = build_html()

        # 5. Send
        current_stage = "Email Delivery"
        send_email("📰 Weekly Logistics Newsletter", html_content)
        
        print("✅ Pipeline completed successfully.")

    except Exception as e:
        error_msg = f"CRITICAL FAILURE in [{current_stage}]: {str(e)}"
        print(f"❌ {error_msg}")
        print(traceback.format_exc())
        
        # Notify User
        notify_failure(current_stage, traceback.format_exc())
        
        # Exit with error code to signal failure to external systems (e.g. CI/CD, Cron)
        exit(1)

if __name__ == "__main__":
    run()
