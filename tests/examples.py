"""Example usage and test module for the Code Review Assistant."""

import sys
from pathlib import Path

# Add parent directory to path for testing
sys.path.insert(0, str(Path(__file__).parent))

from git_handler import GitHandler
from ollama_client import OllamaClient
from tui import ReviewTUI


def demo_tui():
    """Demonstrate TUI components."""
    tui = ReviewTUI()

    tui.show_banner()

    # Demo repo status
    tui.show_info("Demo: Repository Status")
    demo_status = {
        'branch': 'main',
        'is_dirty': True,
        'untracked_count': 2,
        'modified_count': 3,
        'staged_count': 1
    }
    tui.show_repo_status(demo_status)

    # Demo connection status
    tui.show_info("Demo: Connection Status")
    tui.show_connection_status(True, True)

    # Demo changes list
    tui.show_info("Demo: Changes List")
    demo_changes = [
        {
            'file': 'main.py',
            'type': 'modified',
            'language': 'python',
            'diff': '+ def new_function():\n+     return True\n'
        },
        {
            'file': 'config.py',
            'type': 'staged',
            'language': 'python',
            'diff': '+ NEW_SETTING = True\n'
        },
        {
            'file': 'test.js',
            'type': 'untracked',
            'language': 'javascript',
            'diff': 'console.log("Hello");\n'
        }
    ]
    tui.show_changes_list(demo_changes)

    # Demo review result
    tui.show_info("Demo: Review Result")
    demo_review = {
        'file': 'main.py',
        'type': 'modified',
        'language': 'python',
        'rating': 'GOOD',
        'review': """
## Overall Assessment
The code changes look solid with good structure.

## Key Issues
- Consider adding docstrings to the new function
- Type hints would improve code clarity

## Suggestions
1. Add input validation
2. Include unit tests
3. Update documentation

## Security Concerns
None identified.

## Rating: GOOD
""",
        'error': False
    }
    tui.show_review_result(demo_review)

    # Demo summary
    tui.show_info("Demo: Review Summary")
    demo_summary = {
        'total_files': 5,
        'errors': 0,
        'ratings': {
            'EXCELLENT': 2,
            'GOOD': 2,
            'FAIR': 1
        },
        'overall': 'GOOD',
        'reviews': []
    }
    tui.show_summary(demo_summary)

    tui.show_success("Demo completed successfully!")


def test_ollama_connection():
    """Test Ollama connection."""
    tui = ReviewTUI()
    tui.show_banner()
    tui.show_info("Testing Ollama connection...")

    client = OllamaClient()

    connected = client.check_connection()
    if connected:
        tui.show_success("Ollama is connected!")

        model_available = client.check_model_available()
        if model_available:
            tui.show_success(f"Model '{client.model}' is available!")

            # Test a quick review
            tui.show_info("Testing AI review...")
            test_code = """
def calculate_sum(a, b):
    return a + b

result = calculate_sum(5, 10)
print(result)
"""
            review = client.review_code("test.py", test_code, "python")
            tui.console.print("\n[bold]Test Review Result:[/bold]")
            tui.console.print(review)
        else:
            tui.show_warning(f"Model '{client.model}' not found. Run: ollama pull {client.model}")
    else:
        tui.show_error("Ollama is not running. Start it with: ollama serve")


def test_git_handler():
    """Test Git handler."""
    tui = ReviewTUI()
    tui.show_banner()
    tui.show_info("Testing Git handler...")

    try:
        handler = GitHandler()
        tui.show_success("Git repository found!")

        status = handler.get_repo_status()
        tui.show_repo_status(status)

        unstaged = handler.get_unstaged_changes()
        tui.show_info(f"Found {len(unstaged)} unstaged change(s)")

        staged = handler.get_staged_changes()
        tui.show_info(f"Found {len(staged)} staged change(s)")

    except ValueError as e:
        tui.show_error(str(e))


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "demo":
            demo_tui()
        elif command == "test-ollama":
            test_ollama_connection()
        elif command == "test-git":
            test_git_handler()
        else:
            print("Unknown command. Use: demo, test-ollama, or test-git")
    else:
        print("Usage: python examples.py [demo|test-ollama|test-git]")
        print("\nAvailable commands:")
        print("  demo        - Show TUI component demonstrations")
        print("  test-ollama - Test Ollama connection and model")
        print("  test-git    - Test Git integration")

