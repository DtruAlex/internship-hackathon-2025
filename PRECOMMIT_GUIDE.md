# Pre-Commit Hook Setup Guide

## Overview

The AI Code Review Assistant now includes an automatic pre-commit hook that reviews your staged changes before each commit. You'll see the AI review streaming in real-time, just like watching ChatGPT respond!

## Quick Installation

```bash
# Run the installation script
./install-hook.sh
```

That's it! The hook is now installed and will run automatically before every commit.

## What Happens During a Commit?

When you run `git commit`, the pre-commit hook will:

1. **Detect staged changes** - Find all files you're about to commit
2. **Start AI review** - Send each file to Ollama for analysis
3. **Stream the review** - Show the AI's review as it's being generated (real-time!)
4. **Show ratings** - Display ratings (EXCELLENT, GOOD, FAIR, NEEDS_WORK)
5. **Provide summary** - Give an overall assessment
6. **Allow/Block commit** - Decide whether to proceed (configurable)

### Example Workflow

```bash
# 1. Make some changes
vim main.py

# 2. Stage the changes
git add main.py

# 3. Try to commit
git commit -m "Add new feature"

# 4. Watch the magic! ✨
🤖 AI Code Review Pre-Commit Hook

Found 1 file(s) to review:
  • main.py (python)

[1/1] Reviewing main.py...

📄 main.py [STAGED] • python • Reviewing...
────────────────────────────────────────────
Overall assessment: The code changes introduce a new
feature that is well-structured and follows Python best
practices. The implementation is clean and maintainable.

Key improvements:
1. Good error handling
2. Clear variable names
3. Proper documentation

Rating: GOOD

✓ Rating: GOOD

📊 Review Summary
─────────────────
Overall Assessment: GOOD

Files Reviewed: 1
Errors: 0

Rating Distribution:
  • GOOD: 1 (100.0%)

✅ Review complete. Proceeding with commit.
[main abc123] Add new feature
 1 file changed, 10 insertions(+)
```

## Configuration Options

### 1. Block Commits with Issues

By default, the hook shows warnings but **allows all commits**. To block commits with quality issues:

```bash
# Set environment variable (temporary)
export BLOCK_ON_ISSUES=true
git commit -m "Your message"

# Or make it permanent
echo 'export BLOCK_ON_ISSUES=true' >> ~/.bashrc
source ~/.bashrc
```

When enabled, commits will be blocked if the review finds:
- Any file with rating: `NEEDS_WORK`
- Any errors during review

### 2. Skip the Hook (Emergency Bypass)

Sometimes you need to commit quickly without review:

```bash
# Skip the hook for this commit only
git commit --no-verify -m "Emergency fix"

# Or use the short form
git commit -n -m "Emergency fix"
```

### 3. Customize the Hook

Edit `.git/hooks/pre-commit` to customize behavior:

```bash
# Edit the hook
vim .git/hooks/pre-commit

# Example: Always block on issues
BLOCK_ON_ISSUES=true

# Example: Use a different model
# (Modify main.py or config.py)
```

## Manual Installation

If you prefer to install manually:

```bash
# Copy the hook
cp pre-commit-hook.sh .git/hooks/pre-commit

# Make it executable
chmod +x .git/hooks/pre-commit

# Test it
git commit --dry-run
```

## Uninstalling

To remove the pre-commit hook:

```bash
# Simply delete the hook file
rm .git/hooks/pre-commit

# Or rename it to disable
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled
```

Your backup (if any) is saved as `.git/hooks/pre-commit.backup.TIMESTAMP`

## Troubleshooting

### Hook doesn't run

**Problem**: Commit happens without review

**Solution**:
```bash
# Check if hook exists and is executable
ls -la .git/hooks/pre-commit

# Make it executable if needed
chmod +x .git/hooks/pre-commit

# Verify it works
.git/hooks/pre-commit
```

### Ollama not running

**Problem**: Warning about Ollama not being available

**Solution**:
```bash
# Start Ollama in a separate terminal
ollama serve

# Or run it in the background
nohup ollama serve > /tmp/ollama.log 2>&1 &
```

### Model not found

**Problem**: Warning about model not being available

**Solution**:
```bash
# Pull the required model
ollama pull llama3.2:1b

# Verify it's installed
ollama list
```

### Python not found

**Problem**: Hook can't find Python

**Solution**:
```bash
# The hook looks for Python in this order:
# 1. .venv/bin/python (virtual environment)
# 2. python3
# 3. python

# Ensure one is available
which python3
which python

# Or create a virtual environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Hook runs too slowly

**Problem**: Review takes too long for large commits

**Solution**:
- Review fewer files at once (commit more frequently)
- Use a faster model (trade-off: less accurate)
- Skip the hook for large refactors: `git commit --no-verify`

### Want to see reviews but not block commits

**Problem**: Hook is too strict

**Solution**:
```bash
# Ensure BLOCK_ON_ISSUES is not set
unset BLOCK_ON_ISSUES

# Or explicitly set it to false
export BLOCK_ON_ISSUES=false
```

## Integration with CI/CD

You can also run the review in your CI/CD pipeline:

```yaml
# .github/workflows/code-review.yml (GitHub Actions example)
name: AI Code Review

on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Install Ollama
        run: |
          curl https://ollama.ai/install.sh | sh
          ollama pull llama3.2:1b
          nohup ollama serve &
          sleep 5
      
      - name: Run Code Review
        run: python main.py --precommit --block-on-issues
```

## Best Practices

1. **Review Early, Review Often**: Commit small changes frequently
2. **Read the Reviews**: Don't just ignore the feedback - learn from it!
3. **Use --no-verify Sparingly**: Only skip reviews in emergencies
4. **Keep Ollama Running**: Start it when you begin coding
5. **Update Regularly**: Keep the AI model and code updated

## Advanced Usage

### Custom Review Prompts

Edit `config.py` to customize what the AI looks for:

```python
SYSTEM_PROMPT = """You are a senior code reviewer specializing in [YOUR_DOMAIN].
Focus especially on [SPECIFIC_CONCERNS]."""
```

### Different Models

Try different Ollama models for speed/quality trade-offs:

```bash
# Faster but less detailed
export OLLAMA_MODEL=llama3.2:1b

# Slower but more thorough
export OLLAMA_MODEL=llama3.2:3b

# Specialized models
export OLLAMA_MODEL=codellama
```

### Multiple Repositories

Install the hook in multiple repositories:

```bash
# In each repository
cd /path/to/repo1
./path/to/haufe-2025-hackathon/install-hook.sh

cd /path/to/repo2
./path/to/haufe-2025-hackathon/install-hook.sh
```

## FAQs

**Q: Will this slow down my commits?**
A: Yes, but you'll save time by catching issues early. The streaming output makes the wait feel much shorter.

**Q: Does my code leave my machine?**
A: No! Everything runs locally through Ollama. Your code never leaves your computer.

**Q: Can I use this with other pre-commit hooks?**
A: Yes! You can combine multiple hooks using a tool like [pre-commit](https://pre-commit.com/).

**Q: What if I'm offline?**
A: The hook will detect that Ollama isn't running and skip the review gracefully.

**Q: Can I customize the review criteria?**
A: Yes! Edit `config.py` to modify the `REVIEW_PROMPT_TEMPLATE` and `SYSTEM_PROMPT`.

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs: `cat /tmp/ollama.log`
3. Test manually: `python main.py --precommit`
4. Open an issue on the project repository

---

**Happy coding with AI-powered reviews! 🚀**

