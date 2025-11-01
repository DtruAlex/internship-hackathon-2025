#!/bin/bash

# Quick Status Check Script
# Run this to verify everything is working

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   AI Code Review Assistant - Status Check                    ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo

# Check Python
echo "🐍 Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "   ✅ $PYTHON_VERSION"
else
    echo "   ❌ Python not found"
fi
echo

# Check Ollama
echo "🤖 Checking Ollama..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   ✅ Ollama is running on localhost:11434"

    # Check for model
    if curl -s http://localhost:11434/api/tags 2>/dev/null | grep -q "llama3.2:1b"; then
        echo "   ✅ LLama 3.2:1B model is available"
    else
        echo "   ⚠️  LLama 3.2:1B model not found"
        echo "      Run: ollama pull llama3.2:1b"
    fi
else
    echo "   ❌ Ollama is not running"
    echo "      Start it with: ollama serve"
fi
echo

# Check Git
echo "📦 Checking Git repository..."
if git rev-parse --git-dir > /dev/null 2>&1; then
    REPO_ROOT=$(git rev-parse --show-toplevel)
    BRANCH=$(git branch --show-current)
    echo "   ✅ Git repository found"
    echo "      Root: $REPO_ROOT"
    echo "      Branch: $BRANCH"
else
    echo "   ❌ Not in a Git repository"
fi
echo

# Check pre-commit hook
echo "🪝 Checking pre-commit hook..."
if [ -f .git/hooks/pre-commit ]; then
    if grep -q "AI Code Review" .git/hooks/pre-commit 2>/dev/null; then
        echo "   ✅ Pre-commit hook is installed"
        echo "      Location: .git/hooks/pre-commit"
        HOOK_SIZE=$(ls -lh .git/hooks/pre-commit | awk '{print $5}')
        echo "      Size: $HOOK_SIZE"
    else
        echo "   ⚠️  Pre-commit hook exists but may not be ours"
    fi
else
    echo "   ❌ Pre-commit hook not installed"
    echo "      Run: ./install-hook.sh"
fi
echo

# Check main files
echo "📄 Checking project files..."
REQUIRED_FILES=(
    "main.py"
    "code_reviewer.py"
    "ollama_client.py"
    "tui.py"
    "config.py"
    "git_handler.py"
    "install-hook.sh"
    "demo-precommit.sh"
)

ALL_PRESENT=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
        ALL_PRESENT=false
    fi
done
echo

# Check documentation
echo "📚 Checking documentation..."
DOC_FILES=(
    "README.md"
    "SHOWCASE.md"
    "PRECOMMIT_GUIDE.md"
    "STREAMING_IMPLEMENTATION.md"
    "IMPLEMENTATION_SUMMARY.md"
)

for file in "${DOC_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ⚠️  $file (optional, but recommended)"
    fi
done
echo

# Check Python dependencies
echo "📦 Checking Python dependencies..."
if python3 -c "import rich" 2>/dev/null; then
    echo "   ✅ rich (TUI library)"
else
    echo "   ❌ rich not installed"
fi

if python3 -c "import ollama" 2>/dev/null; then
    echo "   ✅ ollama (AI client)"
else
    echo "   ❌ ollama not installed"
fi

if python3 -c "import git" 2>/dev/null; then
    echo "   ✅ GitPython (git operations)"
else
    echo "   ❌ GitPython not installed"
fi
echo

# Summary
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   Summary                                                     ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo

# Determine overall status
PYTHON_OK=false
OLLAMA_OK=false
MODEL_OK=false
HOOK_OK=false

command -v python3 &> /dev/null && PYTHON_OK=true
curl -s http://localhost:11434/api/tags > /dev/null 2>&1 && OLLAMA_OK=true
curl -s http://localhost:11434/api/tags 2>/dev/null | grep -q "llama3.2:1b" && MODEL_OK=true
[ -f .git/hooks/pre-commit ] && grep -q "AI Code Review" .git/hooks/pre-commit 2>/dev/null && HOOK_OK=true

if $PYTHON_OK && $OLLAMA_OK && $MODEL_OK && $HOOK_OK; then
    echo "🎉 Status: READY TO USE!"
    echo ""
    echo "Everything is set up correctly. Try it now:"
    echo ""
    echo "   # Run the demo"
    echo "   ./demo-precommit.sh"
    echo ""
    echo "   # Or make a real commit"
    echo "   git add your_file.py"
    echo "   git commit -m 'Your message'"
    echo ""
    echo "   # Watch the AI review stream in real-time! ✨"
elif ! $HOOK_OK; then
    echo "⚠️  Status: HOOK NOT INSTALLED"
    echo ""
    echo "The project is ready, but the pre-commit hook isn't installed."
    echo "Run this to install it:"
    echo ""
    echo "   ./install-hook.sh"
elif ! $OLLAMA_OK; then
    echo "⚠️  Status: OLLAMA NOT RUNNING"
    echo ""
    echo "Start Ollama in a separate terminal:"
    echo ""
    echo "   ollama serve"
elif ! $MODEL_OK; then
    echo "⚠️  Status: MODEL NOT AVAILABLE"
    echo ""
    echo "Pull the required model:"
    echo ""
    echo "   ollama pull llama3.2:1b"
else
    echo "⚠️  Status: SETUP INCOMPLETE"
    echo ""
    echo "Please check the issues above and fix them."
    echo "Refer to PRECOMMIT_GUIDE.md for help."
fi

echo ""
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║   Documentation                                               ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""
echo "📖 SHOWCASE.md              - Visual demo and examples"
echo "📖 PRECOMMIT_GUIDE.md       - Setup and troubleshooting"
echo "📖 STREAMING_IMPLEMENTATION.md - Technical details"
echo "📖 IMPLEMENTATION_SUMMARY.md   - Feature overview"
echo ""

