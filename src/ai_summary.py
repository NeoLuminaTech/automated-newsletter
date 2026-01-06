import os
from openai import OpenAI

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    client = None

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

    if not client or not client.api_key:
        return "⚠️ Mock AI Summary: This is a simulated summary because OPENAI_API_KEY is missing. The article discusses key logistics trends."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"⚠️ OpenAI API Error: {e}")
        return "Error generating summary."
