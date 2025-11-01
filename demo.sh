#!/bin/bash

# Visual demo script for presentations

clear

echo "════════════════════════════════════════════════════════════════"
echo "   AI CODE REVIEW ASSISTANT - DEMO SHOWCASE"
echo "   Powered by Ollama + LLama 3.2:1B"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "This demo will showcase the key features of the application."
echo ""
read -p "Press Enter to continue..."

clear
echo ""
echo "📋 DEMO STEP 1: Project Overview"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "✨ Features:"
echo "  • AI-powered code reviews using LLama 3.2:1B"
echo "  • Beautiful TUI with Rich library"
echo "  • Smart Git integration"
echo "  • Parallel processing for speed"
echo "  • 100% local - your code never leaves your machine"
echo ""
echo "📁 Repository: haufe-2025-hackathon"
echo "🛠️  Technologies: Python, Rich, GitPython, Ollama"
echo ""
read -p "Press Enter to continue..."

clear
echo ""
echo "🎨 DEMO STEP 2: Beautiful TUI Components"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Running demo to show UI components..."
echo ""
sleep 1

source .venv/bin/activate
python examples.py demo

read -p "Press Enter to continue..."

clear
echo ""
echo "🔍 DEMO STEP 3: Git Integration"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Testing Git repository detection..."
echo ""
sleep 1

python examples.py test-git

read -p "Press Enter to continue..."

clear
echo ""
echo "🤖 DEMO STEP 4: Ollama Connection"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Testing AI model connection..."
echo ""
sleep 1

python examples.py test-ollama

read -p "Press Enter to continue..."

clear
echo ""
echo "🧪 DEMO STEP 5: Test Suite"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Running comprehensive test suite..."
echo ""
sleep 1

./test.sh

read -p "Press Enter to continue..."

clear
echo ""
echo "📊 DEMO STEP 6: Project Structure"
echo "═══════════════════════════════════════════════════════════════"
echo ""
tree -L 1 -I '.venv|.git|.idea|__pycache__' --dirsfirst

echo ""
echo "Key Files:"
echo "  • main.py              - Application entry point"
echo "  • code_reviewer.py     - Core review logic"
echo "  • git_handler.py       - Git operations"
echo "  • ollama_client.py     - AI integration"
echo "  • tui.py              - Terminal UI"
echo "  • config.py           - Configuration"
echo ""
read -p "Press Enter to continue..."

clear
echo ""
echo "📚 DEMO STEP 7: Documentation"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Available Documentation:"
echo ""
echo "  📖 README.md            - Main documentation"
echo "  🚀 QUICKSTART.md        - Quick start guide"
echo "  👨‍💻 DEVELOPER_GUIDE.md   - Developer documentation"
echo "  📋 PROJECT_OVERVIEW.md  - Project summary"
echo "  🤝 CONTRIBUTING.md      - Contribution guidelines"
echo "  ✅ COMPLETION_REPORT.md - Project completion report"
echo ""
read -p "Press Enter to continue..."

clear
echo ""
echo "🎯 DEMO STEP 8: Real Usage Example"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Let's see how to use the application:"
echo ""
echo "1️⃣  First-time setup:"
echo "   ./setup.sh"
echo ""
echo "2️⃣  Start Ollama (in separate terminal):"
echo "   ollama serve"
echo ""
echo "3️⃣  Run interactive mode:"
echo "   ./run.sh --interactive"
echo ""
echo "4️⃣  Or quick review:"
echo "   ./run.sh"
echo ""
echo "5️⃣  Review staged changes:"
echo "   ./run.sh --staged"
echo ""
read -p "Press Enter to continue..."

clear
echo ""
echo "💡 DEMO STEP 9: Key Differentiators"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Why This Project Stands Out:"
echo ""
echo "  ✅ 100% Local - No external API calls, complete privacy"
echo "  ✅ Beautiful UI - Professional TUI with Rich"
echo "  ✅ Fast - Parallel processing, optimized for speed"
echo "  ✅ Smart - Handles edge cases, robust error handling"
echo "  ✅ Documented - Comprehensive guides and examples"
echo "  ✅ Tested - Full test suite with all tests passing"
echo "  ✅ Production Ready - Can be used immediately"
echo ""
read -p "Press Enter to continue..."

clear
echo ""
echo "🎓 DEMO STEP 10: Use Cases"
echo "═══════════════════════════════════════════════════════════════"
echo ""
echo "Perfect for:"
echo ""
echo "  📝 Pre-commit reviews - Catch issues before they enter VCS"
echo "  🎓 Learning - Get instant feedback to improve skills"
echo "  👥 Team standards - Ensure consistent code quality"
echo "  🔒 Security - Identify potential vulnerabilities"
echo "  📈 Code quality - Maintain high standards"
echo ""
read -p "Press Enter to continue..."

clear
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "   ✅ DEMO COMPLETE!"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🎉 The AI Code Review Assistant is ready to use!"
echo ""
echo "Quick Start:"
echo "  1. ./setup.sh               # One-time setup"
echo "  2. ollama serve             # Start AI (separate terminal)"
echo "  3. ./run.sh --interactive   # Start reviewing!"
echo ""
echo "📚 Documentation: Check README.md and QUICKSTART.md"
echo "🧪 Testing: Run ./test.sh"
echo "💡 Examples: Run python examples.py demo"
echo ""
echo "Built with ❤️  for Haufe 2025 Hackathon"
echo ""

