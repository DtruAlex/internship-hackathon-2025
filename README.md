```
    ╔═══════════════════════════════════════════════════════════════╗
    ║                                                               ║
    ║        🤖  AI CODE REVIEW ASSISTANT  🤖                       ║
    ║                                                               ║
    ║        Pre-commit Code Reviews with Local AI                 ║
    ║        Powered by Ollama + LLama 3.2:1B                      ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
```

A powerful TUI (Text User Interface) application that performs intelligent code reviews before you commit, powered by Ollama and LLama 3.2:1B.

**🎯 Built for Haufe 2025 Hackathon**

---

## ⚡ NEW: Real-Time Streaming Pre-Commit Hook!

**Watch the AI review your code as it's being generated - just like ChatGPT!**

```bash
# Install in 1 command
./install-hook.sh

# Every commit now gets an AI review with live streaming!
git commit -m "Your message"
# 🤖 AI reviews your code in real-time ✨
```

👉 **[See it in action - SHOWCASE.md](SHOWCASE.md)** | **[Setup Guide - PRECOMMIT_GUIDE.md](PRECOMMIT_GUIDE.md)**

---

## Features

- 🔍 **Smart Git Integration** - Automatically detects unstaged and staged changes
- 🤖 **AI-Powered Reviews** - Uses LLama 3.2:1B via Ollama for intelligent code analysis
- ✨ **Real-Time Streaming** - Watch the AI review your code as it's being generated!
- 🪝 **Pre-Commit Hook** - Automatic code review before every commit
- 🎨 **Beautiful TUI** - Rich terminal interface with syntax highlighting
- 📊 **Detailed Feedback** - Get suggestions on code quality, bugs, security, and best practices
- ⚡ **Fast & Local** - All processing happens locally with Ollama

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- LLama 3.2:1B model pulled (`ollama pull llama3.2:1b`)

## Installation

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure Ollama is running with LLama 3.2:1B:
```bash
ollama pull llama3.2:1b
ollama serve
```

## Quick Start

### Option 1: Automatic Pre-Commit Hook (Recommended)

Install the pre-commit hook to automatically review code before every commit:

```bash
./install-hook.sh
```

Now every `git commit` will trigger an AI review with real-time streaming! ✨

See [PRECOMMIT_GUIDE.md](PRECOMMIT_GUIDE.md) for detailed setup and configuration.

### Option 2: Manual Interactive Mode

Navigate to your git repository and run:

```bash
python main.py --interactive
```

Or review staged changes directly:

```bash
python main.py --staged
```

Or run as a pre-commit hook manually:

```bash
python main.py --precommit
```

### Available Commands

- **Interactive Mode**: Choose what to review with a menu
- **Review Unstaged Changes**: See AI feedback on uncommitted work
- **Review Staged Changes**: Check what's about to be committed
- **Pre-Commit Mode**: Streaming review with optional commit blocking
- **Repository Status**: View current git status

## Documentation

- 📖 **[Pre-Commit Hook Guide](PRECOMMIT_GUIDE.md)** - Complete setup and configuration guide
- 🔧 **[Streaming Implementation](STREAMING_IMPLEMENTATION.md)** - Technical details of streaming reviews
- 📋 **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Overview of all features
- 🚀 **[Quick Start](QUICKSTART.md)** - Get started in minutes
- 👨‍💻 **[Developer Guide](DEVELOPER_GUIDE.md)** - Contribute to the project

## Configuration

Edit `config.py` to customize:
- AI model selection
- Review criteria
- Output format
- Max diff size

## Project Structure

```
.
├── main.py              # Entry point
├── code_reviewer.py     # Core review logic
├── git_handler.py       # Git operations
├── ollama_client.py     # Ollama API client
├── tui.py              # Rich TUI interface
├── config.py           # Configuration
└── requirements.txt    # Dependencies
```

## License

MIT License
rich>=13.7.0
ollama>=0.1.7
gitpython>=3.1.40
prompt-toolkit>=3.0.43

