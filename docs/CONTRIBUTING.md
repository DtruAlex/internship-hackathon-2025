# Contributing to AI Code Review Assistant

Thank you for considering contributing to this project! 🎉

## How to Contribute

### Reporting Issues
- Use the issue tracker for bug reports and feature requests
- Describe the issue clearly with steps to reproduce
- Include your environment details (OS, Python version, Ollama version)

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow PEP 8 style guidelines
   - Add docstrings to functions and classes
   - Keep functions focused and modular
   - Add type hints where appropriate

4. **Test your changes**
   ```bash
   python examples.py test-ollama
   python examples.py test-git
   python main.py --interactive
   ```

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: description of your feature"
   ```

6. **Push and create a Pull Request**

## Development Setup

```bash
# Clone the repository
git clone <repo-url>
cd haufe-2025-hackathon

# Run setup
./setup.sh

# Activate virtual environment
source .venv/bin/activate

# Make your changes
# ...

# Test before committing
python examples.py demo
```

## Code Style

- Follow PEP 8
- Use meaningful variable names
- Add comments for complex logic
- Keep functions under 50 lines when possible
- Use type hints

## Project Structure

```
├── main.py              # Entry point
├── code_reviewer.py     # Core review logic
├── git_handler.py       # Git operations
├── ollama_client.py     # Ollama API client
├── tui.py              # Rich TUI interface
├── config.py           # Configuration
└── examples.py         # Testing utilities
```

## Adding New Features

### Adding a New Review Criteria
Edit `config.py`:
```python
REVIEW_ASPECTS = [
    "Code quality and readability",
    "Your new criteria here",
    # ...
]
```

### Adding a New Language
Edit `git_handler.py` in `_detect_language()` method:
```python
ext_map = {
    '.py': 'python',
    '.your_ext': 'your_language',
    # ...
}
```

### Adding New TUI Components
Add methods to `tui.py` following the existing pattern.

## Testing

Before submitting:
1. Test with actual git repositories
2. Test with different file types
3. Test error handling
4. Run the demo: `python examples.py demo`

## Questions?

Feel free to open an issue for discussion!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

