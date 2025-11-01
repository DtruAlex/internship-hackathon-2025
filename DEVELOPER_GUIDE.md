# AI Code Review Assistant - Developer Guide

## Architecture Overview

This application follows a modular architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────┐
│              main.py (Entry Point)          │
│          CodeReviewApp (Orchestrator)       │
└─────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        │           │           │
        ▼           ▼           ▼
    ┌──────┐   ┌──────┐   ┌──────┐
    │ TUI  │   │ Code │   │ Git  │
    │      │   │Review│   │Handle│
    │      │   │  er  │   │  r   │
    └──────┘   └──────┘   └──────┘
                    │
                    ▼
              ┌──────────┐
              │  Ollama  │
              │  Client  │
              └──────────┘
                    │
                    ▼
              ┌──────────┐
              │  Ollama  │
              │  Server  │
              └──────────┘
```

## Components

### 1. main.py - Application Entry Point
- Orchestrates the entire application
- Handles CLI arguments
- Manages interactive and quick-review modes

### 2. tui.py - Terminal User Interface
- Built with Rich library
- Provides beautiful, colorful terminal UI
- Components:
  - Banner display
  - Repository status
  - Progress bars
  - Review results formatting
  - Interactive menus

### 3. git_handler.py - Git Integration
- Uses GitPython library
- Functions:
  - Detect unstaged changes
  - Detect staged changes
  - Get file diffs
  - Filter excluded files
  - Language detection

### 4. ollama_client.py - AI Integration
- Communicates with Ollama API
- Functions:
  - Connection checking
  - Model availability checking
  - Code review requests
  - Response parsing

### 5. code_reviewer.py - Review Orchestration
- Coordinates reviews across multiple files
- Parallel processing with ThreadPoolExecutor
- Rating extraction and summary generation

### 6. config.py - Configuration
- Centralized settings
- Easily customizable parameters
- Prompts and templates

## Usage Examples

### Basic Usage

```bash
# Review unstaged changes
python main.py

# Review staged changes
python main.py --staged

# Interactive mode
python main.py --interactive

# Specific repository
python main.py --repo-path /path/to/repo
```

### Using Helper Scripts

```bash
# Setup everything
./setup.sh

# Quick run
./run.sh --interactive
```

### Testing Components

```bash
# Test Ollama connection
python examples.py test-ollama

# Test Git integration
python examples.py test-git

# Demo UI components
python examples.py demo
```

## Customization

### Changing the AI Model

Edit `config.py`:
```python
OLLAMA_MODEL = "llama3.2:3b"  # Use larger model
```

### Adjusting Review Criteria

Edit `config.py`:
```python
REVIEW_ASPECTS = [
    "Code quality",
    "Security",
    "Performance",
    # Add your own criteria
]
```

### Custom Prompts

Modify `SYSTEM_PROMPT` and `REVIEW_PROMPT_TEMPLATE` in `config.py` to customize how the AI reviews code.

### Exclude Patterns

Add patterns to `EXCLUDE_PATTERNS` in `config.py`:
```python
EXCLUDE_PATTERNS = [
    "*.lock",
    "build/*",
    "node_modules/*",
]
```

## How It Works

### 1. Initialization
- Check for Git repository
- Verify Ollama connection
- Verify model availability

### 2. Change Detection
- Scan for modified, staged, or untracked files
- Filter based on exclude patterns
- Detect programming language

### 3. Review Process
- Group files into batches
- Send each file's diff to AI
- Process reviews in parallel
- Extract ratings and issues

### 4. Results Presentation
- Display individual file reviews
- Show overall summary
- Provide actionable feedback

## Advanced Features

### Parallel Processing
Reviews are processed in parallel using ThreadPoolExecutor, with batch size configurable in `config.py`.

### Language Detection
Automatic language detection based on file extension for proper syntax highlighting and context.

### Smart Truncation
Large diffs are truncated to prevent overwhelming the AI model while keeping essential information.

## Integration Ideas

### Pre-commit Hook
Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python main.py --staged
exit 0  # Always allow commit
```

### CI/CD Integration
```yaml
# .github/workflows/review.yml
- name: AI Code Review
  run: |
    pip install -r requirements.txt
    python main.py --staged
```

### Git Alias
```bash
git config --global alias.ai-review '!python /path/to/main.py'
# Usage: git ai-review
```

## Performance Tuning

### For Faster Reviews
- Reduce `MAX_DIFF_SIZE` in config
- Increase `REVIEW_BATCH_SIZE`
- Use smaller model (llama3.2:1b)

### For Better Quality
- Use larger model (llama3.2:3b or llama3.2)
- Increase `num_predict` in ollama_client.py
- Reduce batch size for more focused reviews

## Troubleshooting

### Ollama Connection Issues
```bash
# Check if running
curl http://localhost:11434/api/tags

# Start Ollama
ollama serve
```

### Model Not Found
```bash
# List available models
ollama list

# Pull required model
ollama pull llama3.2:1b
```

### Git Issues
```bash
# Verify you're in a git repo
git status

# Check current directory
pwd
```

### Python Issues
```bash
# Verify Python version (need 3.8+)
python3 --version

# Reinstall dependencies
pip install -r requirements.txt
```

## Contributing

Feel free to extend this application with:
- Additional AI models support
- Export functionality (JSON, HTML reports)
- Integration with code quality tools
- Support for pull request reviews
- Web interface
- VS Code extension

## Future Enhancements

- [ ] Export reviews to JSON/HTML
- [ ] Integration with GitHub/GitLab APIs
- [ ] Code fix suggestions
- [ ] Historical review tracking
- [ ] Custom rule definitions
- [ ] Multi-model comparison
- [ ] Team review collaboration
- [ ] Statistics and metrics dashboard

