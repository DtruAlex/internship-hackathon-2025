# Quick Start Guide

## Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running
3. **Git repository** (to review changes)

## Installation Steps

### 1. Install Ollama (if not already installed)

**Linux/macOS:**
```bash
curl https://ollama.ai/install.sh | sh
```

**Or download from:** https://ollama.ai/

### 2. Pull the LLama 3.2:1B Model

```bash
ollama pull llama3.2:1b
```

### 3. Start Ollama Server

```bash
ollama serve
```

Keep this terminal open. Ollama needs to be running in the background.

### 4. Set Up the Application

In a new terminal:

```bash
# Navigate to the project directory
cd /home/dumi/Projects/haufe-2025-hackathon

# Run the setup script
./setup.sh
```

This will:
- Create a virtual environment
- Install all Python dependencies
- Verify Ollama is running
- Check for the model

## Usage

### Interactive Mode (Recommended for First Use)

```bash
./run.sh --interactive
```

Or:

```bash
source .venv/bin/activate
python main.py --interactive
```

This will:
1. Show repository status
2. Present a menu with options
3. Let you choose what to review
4. Display results with ratings

### Quick Review Mode

Review unstaged changes:
```bash
./run.sh
```

Review staged changes:
```bash
./run.sh --staged
```

## Example Workflow

### Scenario 1: Before Committing

```bash
# Make some changes to your code
vim myfile.py

# Review your unstaged changes
./run.sh

# If everything looks good, stage and commit
git add .
git commit -m "Your commit message"
```

### Scenario 2: Review Before Push

```bash
# Stage your changes
git add .

# Review what you're about to commit
./run.sh --staged

# If approved, commit
git commit -m "Your commit message"
```

### Scenario 3: Interactive Exploration

```bash
# Start interactive mode
./run.sh --interactive

# Choose from menu:
# 1. Review unstaged changes
# 2. Review staged changes
# 3. Show repository status
# 4. Exit
```

## Testing the Installation

### Test 1: Check Ollama Connection

```bash
python examples.py test-ollama
```

Expected output:
- ✅ Ollama is connected!
- ✅ Model 'llama3.2:1b' is available!
- Test review result shown

### Test 2: Check Git Integration

```bash
python examples.py test-git
```

Expected output:
- ✅ Git repository found!
- Repository status displayed
- Number of changes detected

### Test 3: Demo UI Components

```bash
python examples.py demo
```

Shows all UI components with sample data.

## Creating Your First Review

1. Make sure you're in a git repository with some changes:
```bash
cd your-project
# Make some changes to files
echo "print('Hello World')" > test.py
```

2. Run the reviewer:
```bash
cd /home/dumi/Projects/haufe-2025-hackathon
./run.sh --repo-path ~/path/to/your-project
```

3. View the AI-generated review with:
   - Overall assessment
   - Issues found
   - Suggestions
   - Security concerns
   - Quality rating

## Troubleshooting

### "Ollama is not running"

**Solution:** Start Ollama in another terminal
```bash
ollama serve
```

### "Model not found"

**Solution:** Pull the model
```bash
ollama pull llama3.2:1b
```

### "Not a git repository"

**Solution:** Make sure you're in a git repository
```bash
git init  # If starting a new repo
# OR
cd /path/to/existing/repo
```

### "No changes found"

**Solution:** Make some changes to files
```bash
echo "# Test change" >> README.md
```

### Import errors

**Solution:** Activate virtual environment and install dependencies
```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Tips for Best Results

1. **Review Small Changes:** AI works best on focused, small changes
2. **Stage Logically:** Group related changes together
3. **Use Regularly:** Make it part of your workflow before each commit
4. **Customize Prompts:** Edit `config.py` to adjust review criteria
5. **Check Ratings:** Pay attention to "NEEDS_WORK" ratings

## Next Steps

- Read the full [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for customization
- Set up a pre-commit hook for automatic reviews
- Customize review prompts in `config.py`
- Try different Ollama models for varying quality/speed

## Getting Help

If you encounter issues:

1. Check this guide first
2. Run the test commands to diagnose
3. Check Ollama logs: `ollama logs`
4. Verify Python version: `python3 --version` (need 3.8+)
5. Check virtual environment: `which python` (should show .venv path)

## Common Use Cases

### Daily Development
```bash
# Before each commit
./run.sh
# Review feedback
# Fix issues if any
git add .
git commit -m "..."
```

### Pull Request Preparation
```bash
# Stage all changes
git add .

# Review everything
./run.sh --staged

# Create PR if all looks good
```

### Learning from AI
Use the reviews to:
- Learn best practices
- Catch bugs early
- Improve code quality
- Discover security issues
- Get documentation suggestions

---

**Enjoy your AI-powered code reviews! 🚀**

