#!/bin/bash

# Pre-commit hook for AI Code Review with Streaming
# This hook runs before every commit to review your staged changes
#
# Installation:
#   ./install-hook.sh
# Or manually:
#   cp pre-commit-hook.sh .git/hooks/pre-commit
#   chmod +x .git/hooks/pre-commit
#
# To skip the hook for one commit:
#   git commit --no-verify

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# If running from .git/hooks/, adjust the path
if [[ "$SCRIPT_DIR" == *".git/hooks"* ]]; then
    REPO_ROOT="$(git rev-parse --show-toplevel)"
    REVIEW_SCRIPT="$REPO_ROOT/main.py"
else
    # Running from repo root
    REVIEW_SCRIPT="$SCRIPT_DIR/main.py"
fi

# Try to find Python (prefer venv if it exists)
if [ -f "$REPO_ROOT/.venv/bin/python" ]; then
    PYTHON="$REPO_ROOT/.venv/bin/python"
elif [ -f "$SCRIPT_DIR/.venv/bin/python" ]; then
    PYTHON="$SCRIPT_DIR/.venv/bin/python"
elif command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    echo "⚠️  Python not found. Skipping AI review."
    exit 0
fi

# Configuration
# Set BLOCK_ON_ISSUES=true to prevent commits with code quality issues
BLOCK_ON_ISSUES=${BLOCK_ON_ISSUES:-false}

# Build command
CMD="$PYTHON $REVIEW_SCRIPT --precommit"

if [ "$BLOCK_ON_ISSUES" = "true" ]; then
    CMD="$CMD --block-on-issues"
fi

# Run the AI code review with streaming output
$CMD

# Capture exit code
EXIT_CODE=$?

# Exit with the same code (0 = allow commit, 1 = block commit)
exit $EXIT_CODE

