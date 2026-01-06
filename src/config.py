import os

# Configuration Constants
LANGUAGE = "en"
FINAL_TOP_ARTICLES = 10

# Strict Environment Variable Validation
REQUIRED_VARS = ["NEWS_API_KEY", "EMAIL_USER", "EMAIL_PASS", "TO_EMAIL"]

def validate_config():
    """
    Validates that all required environment variables are set.
    Raises EnvironmentError if any are missing.
    """
    missing = [var for var in REQUIRED_VARS if not os.getenv(var)]
    if missing:
        raise EnvironmentError(f"Missing required environment variables: {', '.join(missing)}")

# Re-exporting for convenience
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
SEARCH_QUERY = os.getenv("SEARCH_QUERY")
