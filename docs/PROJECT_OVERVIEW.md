# AI Code Review Assistant - Project Overview

## 🎯 Project Summary

A powerful, local-first TUI application that provides intelligent AI-powered code reviews before you commit. Built for the Haufe 2025 Hackathon, this tool integrates seamlessly with your Git workflow to help catch bugs, improve code quality, and learn best practices.

## ✨ Key Features

- **🤖 AI-Powered Analysis**: Uses LLama 3.2:1B via Ollama for intelligent, context-aware code reviews
- **🎨 Beautiful TUI**: Rich terminal interface with syntax highlighting and intuitive navigation
- **⚡ Fast & Local**: All processing happens on your machine - no data leaves your computer
- **🔍 Smart Git Integration**: Automatically detects and analyzes changes (staged/unstaged/untracked)
- **📊 Detailed Feedback**: Get actionable suggestions on bugs, security, performance, and best practices
- **🔄 Parallel Processing**: Reviews multiple files simultaneously for speed
- **🎯 Customizable**: Easy configuration for prompts, models, and review criteria

## 📁 Project Structure

```
haufe-2025-hackathon/
├── main.py                 # Application entry point and orchestration
├── code_reviewer.py        # Core review logic with parallel processing
├── git_handler.py          # Git operations and file detection
├── ollama_client.py        # Ollama API integration
├── tui.py                 # Rich-based terminal user interface
├── config.py              # Centralized configuration
├── examples.py            # Testing and demonstration utilities
├── requirements.txt       # Python dependencies
├── setup.sh              # Automated setup script
├── run.sh                # Quick run wrapper
├── test.sh               # Comprehensive test suite
├── pre-commit-hook.sh    # Git pre-commit hook template
├── README.md             # Main documentation
├── QUICKSTART.md         # Quick start guide
├── DEVELOPER_GUIDE.md    # Detailed developer documentation
├── CONTRIBUTING.md       # Contribution guidelines
└── LICENSE               # MIT License
```

## 🚀 Quick Start

```bash
# 1. Setup (one time)
./setup.sh

# 2. Start Ollama (in separate terminal)
ollama serve

# 3. Run the app
./run.sh --interactive
```

## 🛠️ Technology Stack

- **Python 3.8+**: Core language
- **Rich**: Beautiful TUI components
- **GitPython**: Git repository interaction
- **Ollama**: Local LLM inference
- **LLama 3.2:1B**: AI model for code review
- **ThreadPoolExecutor**: Parallel review processing

## 📊 Architecture

```
User
  ↓
main.py (CodeReviewApp)
  ↓
├─→ tui.py (ReviewTUI)           # User interface
├─→ code_reviewer.py              # Review orchestration
│   ├─→ ollama_client.py         # AI communication
│   └─→ git_handler.py           # Git operations
└─→ config.py                     # Configuration
```

## 🎓 Use Cases

1. **Pre-Commit Reviews**: Catch issues before they enter version control
2. **Learning Tool**: Get instant feedback on your code to improve skills
3. **Team Standards**: Ensure code follows best practices
4. **Security Scanning**: Identify potential security vulnerabilities
5. **Code Quality**: Maintain high standards across your codebase

## 🔧 Configuration

All settings in `config.py`:

- **Model Selection**: Choose different Ollama models
- **Review Criteria**: Customize what to check
- **Batch Size**: Adjust parallel processing
- **Prompts**: Tailor AI behavior
- **Exclusions**: Skip certain files

## 📈 Performance

- **Speed**: ~2-5 seconds per file (depending on model and file size)
- **Parallel Processing**: Reviews up to 5 files simultaneously
- **Resource Efficient**: LLama 3.2:1B requires minimal resources
- **Smart Truncation**: Handles large files gracefully

## 🧪 Testing

```bash
# Run all tests
./test.sh

# Test specific components
python examples.py test-ollama   # Test AI connection
python examples.py test-git      # Test Git integration
python examples.py demo          # Demo UI components
```

## 🔒 Privacy & Security

- **100% Local**: No data sent to external servers
- **Open Source**: Fully transparent code
- **Your Control**: You own and control all data
- **No Tracking**: No analytics or telemetry

## 🎯 Future Enhancements

Potential additions:
- [ ] Export reviews to JSON/HTML/PDF
- [ ] Integration with GitHub/GitLab APIs
- [ ] Automated fix suggestions
- [ ] Historical review tracking
- [ ] VS Code/JetBrains plugins
- [ ] Multi-model comparison
- [ ] Team collaboration features
- [ ] Custom rule engines
- [ ] CI/CD integration
- [ ] Web dashboard

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Haufe 2025 Hackathon for the opportunity
- Ollama team for the amazing local LLM platform
- Meta for the LLama models
- Rich library for beautiful terminal UI
- GitPython for seamless Git integration

## 📞 Support

- Check [QUICKSTART.md](QUICKSTART.md) for setup help
- See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) for detailed docs
- Run `./test.sh` to diagnose issues
- Open an issue for bug reports

## 🎉 Getting Started

Ready to transform your code review process?

```bash
./setup.sh
./run.sh --interactive
```

Happy coding! 🚀

---

**Built with ❤️ for the Haufe 2025 Hackathon**

