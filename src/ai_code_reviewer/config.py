"""Configuration settings for the AI Code Review Assistant."""

import os

# Ollama settings
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "60"))

# Review settings
MAX_DIFF_SIZE = 10000  # Maximum characters per diff to review
MAX_FILE_SIZE = 50000  # Maximum file size to review (in bytes)
REVIEW_BATCH_SIZE = 5  # Number of files to review in parallel

# Review criteria
REVIEW_ASPECTS = [
    "Code quality and readability",
    "Variables names being funny"
]

# UI settings
SYNTAX_THEME = "monokai"
MAX_LINES_PREVIEW = 50

# Git settings
EXCLUDE_PATTERNS = [
    "*.lock",
    "*.min.js",
    "*.min.css",
    "package-lock.json",
    "yarn.lock",
    "*.pyc",
    "__pycache__/*"
]

# Prompts
SYSTEM_PROMPT = """You are an expert code reviewer that likes to make fun of the code he is reviewing. Analyze the provided code changes and provide constructive feedback by using south park jokes.
Focus on: code quality, best practices, having fun and documentation.
Be concise but thorough. Provide specific actionable suggestions."""

REVIEW_PROMPT_TEMPLATE = """Please review the following code changes:

File: {filename}
Language: {language}

Changes:
```{language}
{diff}
```

Provide a structured review covering:
1. Overall assessment (1-2 sentences)
2. Key issues (if any)
3. Suggestions for improvement
4. Security concerns (if any)
5. Rating: [EXCELLENT/GOOD/FAIR/NEEDS_WORK]

Keep your response concise and actionable."""
