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

# Get the repository root
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

# Path to the ai-code-review script
REVIEW_SCRIPT="$REPO_ROOT/ai-code-review"

# Try to find Python (prefer venv if it exists)
if [ -f "$REPO_ROOT/.venv/bin/python" ]; then
    PYTHON="$REPO_ROOT/.venv/bin/python"
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
if [ -x "$REVIEW_SCRIPT" ]; then
    # Use the entry point script if it exists
    CMD="$REVIEW_SCRIPT --precommit"
else
    # Fall back to running the module directly
    CMD="$PYTHON -m ai_code_reviewer --precommit"
fi

if [ "$BLOCK_ON_ISSUES" = "true" ]; then
    CMD="$CMD --block-on-issues"
fi

# Run the AI code review with streaming output
$CMD

# Capture exit code
EXIT_CODE=$?

# Exit with the same code (0 = allow commit, 1 = block commit)
exit $EXIT_CODE

