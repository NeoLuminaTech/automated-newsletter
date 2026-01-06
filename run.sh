#!/bin/bash

# Load secrets from .env file if it exists
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
  echo "✅ Loaded environment variables from .env"
else
  echo "⚠️ .env file not found. Running with available environment variables."
fi

# Run the newsletter build script
python3 src/build_newsletter.py
