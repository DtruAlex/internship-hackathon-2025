"""AI Code Review Assistant - A tool for automated code review using local AI models."""

__version__ = "1.0.0"
__author__ = "Haufe 2025 Hackathon Team"
__description__ = "Pre-commit code reviews with local AI powered by Ollama + LLama 3.2:1B"

from .code_reviewer import CodeReviewer
from .git_handler import GitHandler
from .ollama_client import OllamaClient
from .tui import ReviewTUI

__all__ = [
    "CodeReviewer",
    "GitHandler", 
    "OllamaClient",
    "ReviewTUI",
]

