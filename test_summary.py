from src.ai_summary import summarize

article = {
    "title": "Test Article",
    "description": "This is a test description."
}

print("Testing summarize fallback...")
summary = summarize(article)
print(f"Summary Result: {summary}")
