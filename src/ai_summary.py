import os
import time
from openai import OpenAI, RateLimitError, APIConnectionError

# Initialize Clients lazily or with error handling during usage?
# Current approach initializes them at module level. 
# If keys are missing, they remain None.

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
    """
    Summarizes an article using OpenAI or DeepSeek.
    Raises RuntimeError if all providers fail.
    """
    prompt = PROMPT_TEMPLATE.format(
        title=article["title"],
        description=article.get("description", "")
    )

    errors = []

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
            msg = f"OpenAI Error ({type(e).__name__}): {e}"
            print(f"⚠️ {msg}. Switching to Fallback (DeepSeek)...")
            errors.append(msg)
        except Exception as e:
             msg = f"OpenAI Unexpected Error: {e}"
             print(f"⚠️ {msg}")
             errors.append(msg)
    else:
        errors.append("OpenAI key missing.")

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
             msg = f"DeepSeek Fallback Error: {e}"
             print(f"⚠️ {msg}")
             errors.append(msg)
    else:
        errors.append("DeepSeek key missing.")

    # 3. Final Fallback: Error
    # Combine errors for context
    error_summary = "; ".join(errors)
    raise RuntimeError(f"All AI summarization providers failed. Details: {error_summary}")
