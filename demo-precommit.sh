#!/bin/bash

# Demo script to showcase the pre-commit hook functionality
# This creates a sample file, commits it, and shows the AI review in action

set -e

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   AI Code Review Pre-Commit Hook - DEMO                   ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo

# Check if hook is installed
if [ ! -f .git/hooks/pre-commit ]; then
    echo "❌ Pre-commit hook not installed!"
    echo "Run: ./install-hook.sh"
    exit 1
fi

echo "✅ Pre-commit hook is installed"
echo

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running!"
    echo "Start it with: ollama serve"
    exit 1
fi

echo "✅ Ollama is running"
echo

# Create a sample Python file with some issues
echo "Creating sample Python file for review..."
cat > demo_sample.py << 'PYEOF'
def calculate_total(items):
    """Calculate total price of items."""
    total = 0
    for item in items:
        total = total + item['price']  # Could use += operator
    return total


def process_data(data):
    """Process data without error handling."""
    result = []
    for d in data:
        # Missing validation
        result.append(d * 2)
    return result


# Missing main guard
print("Processing...")
PYEOF

echo "✅ Created demo_sample.py with some code quality issues"
echo

# Add the file to git
echo "Staging the file..."
git add demo_sample.py
echo

# Show what will happen
echo "════════════════════════════════════════════════════════════"
echo "Now attempting to commit..."
echo "The pre-commit hook will automatically review the code!"
echo "════════════════════════════════════════════════════════════"
echo
sleep 2

# Try to commit (this will trigger the pre-commit hook)
echo "Running: git commit -m 'Add sample code'"
echo
git commit -m "Add sample code for demo"

# Show the result
echo
echo "════════════════════════════════════════════════════════════"
echo "✅ Demo complete!"
echo
echo "The AI reviewed your code before committing!"
echo "You saw the review streaming in real-time! ✨"
echo
echo "To clean up the demo:"
echo "  git reset HEAD~1    # Undo the commit"
echo "  rm demo_sample.py   # Remove the sample file"
echo "════════════════════════════════════════════════════════════"

