#!/bin/bash

# Quick run script for AI Code Review Assistant

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./setup.sh first."
    exit 1
fi

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running. Starting Ollama..."
    echo "Please run in another terminal: ollama serve"
    echo ""
fi

# Run the application
python main.py "$@"

