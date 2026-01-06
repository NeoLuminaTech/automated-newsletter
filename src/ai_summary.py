import os
import time
from openai import OpenAI, RateLimitError, APIConnectionError

# Primary Client: OpenAI
try:
    openai_client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        max_retries=1
    )
except Exception:
    openai_client = None

# Fallback Client: DeepSeek
try:
    deepseek_client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
        max_retries=1
    )
except Exception:
    deepseek_client = None

PROMPT_TEMPLATE = """
Summarize the following logistics news article in 2–3 bullet points.
Focus on business impact, technology, sustainability, or operations.

Title: {title}
Description: {description}
"""

def summarize(article):
    prompt = PROMPT_TEMPLATE.format(
        title=article["title"],
        description=article.get("description", "")
    )

    # 1. Try OpenAI
    if openai_client and openai_client.api_key:
        try:
            response = openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return response.choices[0].message.content
        except (RateLimitError, APIConnectionError) as e:
            print(f"⚠️ OpenAI Error ({type(e).__name__}). Switching to Fallback (DeepSeek)...")
        except Exception as e:
             print(f"⚠️ OpenAI Unexpected Error: {e}")

    # 2. Fallback: DeepSeek
    if deepseek_client and deepseek_client.api_key:
        try:
            response = deepseek_client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as e:
             print(f"⚠️ DeepSeek Fallback Error: {e}")

    # 3. Final Fallback: Mock/Error
    return "⚠️ Summary unavailable (All AI providers failed or missing keys)."
