#!/bin/bash

# Installation script for AI Code Review Pre-Commit Hook
# This script installs the pre-commit hook into your .git/hooks directory

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   AI Code Review Pre-Commit Hook Installation              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${RED}❌ Error: Not in a git repository${NC}"
    exit 1
fi

REPO_ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"
PRE_COMMIT_HOOK="$HOOKS_DIR/pre-commit"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_HOOK="$SCRIPT_DIR/pre-commit-hook.sh"

echo -e "${YELLOW}Repository: ${NC}$REPO_ROOT"
echo -e "${YELLOW}Hooks directory: ${NC}$HOOKS_DIR"
echo

# Check if hook already exists
if [ -f "$PRE_COMMIT_HOOK" ]; then
    echo -e "${YELLOW}⚠️  Pre-commit hook already exists.${NC}"

    # Check if it's our hook
    if grep -q "AI Code Review" "$PRE_COMMIT_HOOK" 2>/dev/null; then
        echo -e "${YELLOW}This appears to be our AI Code Review hook.${NC}"
    else
        echo -e "${YELLOW}This appears to be a different hook.${NC}"
    fi

    read -p "Do you want to replace it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${RED}Installation cancelled.${NC}"
        exit 1
    fi

    # Backup existing hook
    BACKUP="$PRE_COMMIT_HOOK.backup.$(date +%Y%m%d_%H%M%S)"
    cp "$PRE_COMMIT_HOOK" "$BACKUP"
    echo -e "${GREEN}✓ Backed up existing hook to: $BACKUP${NC}"
fi

# Copy the hook
echo -e "${CYAN}Installing pre-commit hook...${NC}"
cp "$SOURCE_HOOK" "$PRE_COMMIT_HOOK"
chmod +x "$PRE_COMMIT_HOOK"

echo -e "${GREEN}✓ Pre-commit hook installed successfully!${NC}"
echo

# Configuration options
echo -e "${CYAN}Configuration Options:${NC}"
echo
echo "The hook will now run automatically before each commit."
echo
echo "To configure the hook behavior, you can set environment variables:"
echo
echo -e "${YELLOW}1. Block commits with issues:${NC}"
echo "   export BLOCK_ON_ISSUES=true"
echo "   (Add to ~/.bashrc or ~/.zshrc to make permanent)"
echo
echo -e "${YELLOW}2. Skip the hook for one commit:${NC}"
echo "   git commit --no-verify"
echo
echo -e "${YELLOW}3. Uninstall the hook:${NC}"
echo "   rm $PRE_COMMIT_HOOK"
echo

# Check prerequisites
echo -e "${CYAN}Checking Prerequisites:${NC}"

# Check Python
if command -v python3 &> /dev/null || command -v python &> /dev/null; then
    echo -e "${GREEN}✓ Python found${NC}"
else
    echo -e "${RED}✗ Python not found${NC}"
    echo "  Please install Python 3.8+"
fi

# Check Ollama
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Ollama is running${NC}"
else
    echo -e "${YELLOW}⚠ Ollama is not running${NC}"
    echo "  Start it with: ollama serve"
fi

# Check if model is available
if curl -s http://localhost:11434/api/tags 2>/dev/null | grep -q "llama3.2:1b"; then
    echo -e "${GREEN}✓ LLama 3.2:1B model is available${NC}"
else
    echo -e "${YELLOW}⚠ LLama 3.2:1B model not found${NC}"
    echo "  Pull it with: ollama pull llama3.2:1b"
fi

echo
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║   Installation Complete!! 🎉                               ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo
echo -e "${CYAN}Next steps:${NC}"
echo "1. Make sure Ollama is running: ${YELLOW}ollama serve${NC}"
echo "2. Make some changes and commit: ${YELLOW}git commit${NC}"
echo "3. Watch the AI review your code in real-time! ✨"
echo

