#!/bin/bash

# Pre-commit hook for AI Code Review
# Copy this to .git/hooks/pre-commit and make it executable

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🤖 Running AI Code Review...${NC}"

# Path to the code review script
REVIEW_SCRIPT="/home/dumi/Projects/haufe-2025-hackathon/main.py"
PYTHON_ENV="/home/dumi/Projects/haufe-2025-hackathon/.venv/bin/python"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  Ollama is not running. Skipping AI review.${NC}"
    echo -e "${YELLOW}Start Ollama with: ollama serve${NC}"
    exit 0
fi

# Run the review on staged changes
$PYTHON_ENV $REVIEW_SCRIPT --staged

# Check if there were any critical issues
# For now, we always allow the commit (exit 0)
# You can modify this to exit 1 to block commits with issues

echo -e "${GREEN}✅ Review complete. Proceeding with commit.${NC}"
exit 0

