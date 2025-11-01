#!/bin/bash

# Comprehensive test script for AI Code Review Assistant

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   AI Code Review Assistant - Test Suite      ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# Activate virtual environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo -e "${GREEN}✅ Virtual environment activated${NC}"
else
    echo -e "${RED}❌ Virtual environment not found${NC}"
    echo -e "${YELLOW}Run ./setup.sh first${NC}"
    exit 1
fi

# Test 1: Python version
echo ""
echo -e "${BLUE}Test 1: Python Version${NC}"
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"
if python3 -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)"; then
    echo -e "${GREEN}✅ Python version is 3.8+${NC}"
else
    echo -e "${RED}❌ Python version must be 3.8 or higher${NC}"
    exit 1
fi

# Test 2: Dependencies
echo ""
echo -e "${BLUE}Test 2: Python Dependencies${NC}"
ALL_DEPS_OK=true

# Check rich
if python3 -c "import rich" 2>/dev/null; then
    echo -e "${GREEN}✅ rich installed${NC}"
else
    echo -e "${RED}❌ rich not found${NC}"
    ALL_DEPS_OK=false
fi

# Check GitPython (import as 'git')
if python3 -c "import git" 2>/dev/null; then
    echo -e "${GREEN}✅ gitpython installed${NC}"
else
    echo -e "${RED}❌ gitpython not found${NC}"
    ALL_DEPS_OK=false
fi

# Check ollama
if python3 -c "import ollama" 2>/dev/null; then
    echo -e "${GREEN}✅ ollama installed${NC}"
else
    echo -e "${RED}❌ ollama not found${NC}"
    ALL_DEPS_OK=false
fi

if [ "$ALL_DEPS_OK" = false ]; then
    echo -e "${YELLOW}Run: pip install -r requirements.txt${NC}"
    exit 1
fi

# Test 3: Ollama connection
echo ""
echo -e "${BLUE}Test 3: Ollama Connection${NC}"
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Ollama is running${NC}"

    # Check for model
    if ollama list | grep -q "llama3.2:1b"; then
        echo -e "${GREEN}✅ LLama 3.2:1B model available${NC}"
    else
        echo -e "${YELLOW}⚠️  LLama 3.2:1B model not found${NC}"
        echo -e "${YELLOW}Run: ollama pull llama3.2:1b${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Ollama not running${NC}"
    echo -e "${YELLOW}Start with: ollama serve${NC}"
fi

# Test 4: Git repository
echo ""
echo -e "${BLUE}Test 4: Git Repository${NC}"
if git rev-parse --git-dir > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Git repository found${NC}"
    BRANCH=$(git branch --show-current 2>/dev/null || echo "detached HEAD")
    echo "Current branch: $BRANCH"
else
    echo -e "${YELLOW}⚠️  Not in a git repository${NC}"
    echo -e "${YELLOW}Initialize with: git init${NC}"
fi

# Test 5: Core modules
echo ""
echo -e "${BLUE}Test 5: Core Modules${NC}"
MODULES=("main" "config" "git_handler" "ollama_client" "code_reviewer" "tui")
ALL_MODULES_OK=true

for module in "${MODULES[@]}"; do
    if python3 -c "import $module" 2>/dev/null; then
        echo -e "${GREEN}✅ $module.py OK${NC}"
    else
        echo -e "${RED}❌ $module.py has errors${NC}"
        python3 -c "import $module" 2>&1 | head -5
        ALL_MODULES_OK=false
    fi
done

# Test 6: Demo functionality
echo ""
echo -e "${BLUE}Test 6: Demo Functionality${NC}"
if python examples.py demo > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Demo runs successfully${NC}"
else
    echo -e "${RED}❌ Demo failed${NC}"
fi

# Test 7: File permissions
echo ""
echo -e "${BLUE}Test 7: Script Permissions${NC}"
for script in setup.sh run.sh pre-commit-hook.sh; do
    if [ -x "$script" ]; then
        echo -e "${GREEN}✅ $script is executable${NC}"
    else
        echo -e "${YELLOW}⚠️  $script not executable${NC}"
        echo -e "${YELLOW}Run: chmod +x $script${NC}"
    fi
done

# Summary
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║              Test Summary                     ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════╝${NC}"

if [ "$ALL_DEPS_OK" = true ] && [ "$ALL_MODULES_OK" = true ]; then
    echo -e "${GREEN}✅ All core tests passed!${NC}"
    echo ""
    echo -e "${GREEN}You're ready to use the AI Code Review Assistant!${NC}"
    echo ""
    echo "Quick start:"
    echo "  ./run.sh --interactive"
    echo ""
    exit 0
else
    echo -e "${RED}❌ Some tests failed${NC}"
    echo ""
    echo "Please fix the issues above before using the application."
    exit 1
fi

