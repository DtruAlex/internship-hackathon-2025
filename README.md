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

## Features

- 🔍 **Smart Git Integration** - Automatically detects unstaged and staged changes
- 🤖 **AI-Powered Reviews** - Uses LLama 3.2:1B via Ollama for intelligent code analysis
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

## Usage

Navigate to your git repository and run:

```bash
python main.py
```

Or use the interactive mode:

```bash
python main.py --interactive
```

### Commands

- Review all unstaged changes
- Review staged changes
- Review specific files
- Get detailed analysis by file
- Export review reports

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

