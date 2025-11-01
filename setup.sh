#!/bin/bash

# Setup script for AI Code Review Assistant

echo "🚀 Setting up AI Code Review Assistant..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo ""
    echo "⚠️  Ollama is not installed."
    echo "📖 Please install Ollama from: https://ollama.ai/"
    echo ""
else
    echo "✅ Ollama found: $(ollama --version)"

    # Check if llama3.2:1b model is available
    if ollama list | grep -q "llama3.2:1b"; then
        echo "✅ LLama 3.2:1B model is available"
    else
        echo ""
        echo "⚠️  LLama 3.2:1B model not found"
        echo "📥 Pulling model... (this may take a few minutes)"
        ollama pull llama3.2:1b

        if [ $? -eq 0 ]; then
            echo "✅ Model pulled successfully"
        else
            echo "❌ Failed to pull model. Please run manually: ollama pull llama3.2:1b"
        fi
    fi
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To use the application:"
echo "  1. Activate the virtual environment: source .venv/bin/activate"
echo "  2. Make sure Ollama is running: ollama serve"
echo "  3. Run the app: python main.py --interactive"
echo ""

