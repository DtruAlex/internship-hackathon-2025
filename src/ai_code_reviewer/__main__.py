"""Command-line interface for AI Code Review Assistant."""

import sys
import argparse

from .code_reviewer import CodeReviewer
from .git_handler import GitHandler
from .ollama_client import OllamaClient
from .tui import ReviewTUI
from . import config


class CodeReviewApp:
    """Main application class."""

    def __init__(self, repo_path: str = None):
        """Initialize the application.

        Args:
            repo_path: Path to git repository
        """
        self.tui = ReviewTUI()

        try:
            self.git_handler = GitHandler(repo_path)
        except ValueError as e:
            self.tui.show_error(str(e))
            sys.exit(1)

        self.ollama_client = OllamaClient()
        self.code_reviewer = CodeReviewer(self.git_handler, self.ollama_client)

    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are met.

        Returns:
            True if everything is ready
        """
        connected = self.ollama_client.check_connection()
        model_available = self.ollama_client.check_model_available() if connected else False

        self.tui.show_connection_status(connected, model_available)

        if not connected:
            self.tui.show_error("Please start Ollama: ollama serve")
            return False

        if not model_available:
            self.tui.show_warning(f"Model '{config.OLLAMA_MODEL}' not found.")
            self.tui.show_info(f"Pull the model with: ollama pull {config.OLLAMA_MODEL}")
            return False

        return True

    def run_interactive(self):
        """Run the application in interactive mode."""
        self.tui.show_banner()

        if not self.check_prerequisites():
            return

        # Show initial repo status
        status = self.git_handler.get_repo_status()
        self.tui.show_repo_status(status)

        while True:
            choice = self.tui.show_menu()

            if choice == "1":
                self.review_unstaged()
            elif choice == "2":
                self.review_staged()
            elif choice == "3":
                status = self.git_handler.get_repo_status()
                self.tui.show_repo_status(status)
            elif choice == "4":
                self.tui.show_info("Goodbye! 👋")
                break

            if choice in ["1", "2"]:
                self.tui.pause()

    def review_unstaged(self):
        """Review unstaged changes."""
        self.tui.show_info("Scanning for unstaged changes...")

        changes = self.git_handler.get_unstaged_changes()

        if not changes:
            self.tui.show_warning("No unstaged changes found.")
            return

        self.tui.show_changes_list(changes)

        if not self.tui.confirm_action(f"\nReview {len(changes)} file(s)?"):
            return

        self.tui.show_info("Starting AI review... Watch the magic happen! ✨")

        reviews = []
        
        # Review each file with streaming output
        for i, change in enumerate(changes, 1):
            self.tui.show_info(f"[{i}/{len(changes)}] Reviewing {change['file']}...")
            self.tui.show_streaming_review_header(
                change['file'],
                change['type'],
                change['language']
            )
            
            # Stream the review
            review_dict = None
            for chunk, is_complete, review_data in self.code_reviewer.review_single_file_streaming(
                change['file'],
                change['diff'],
                change['language'],
                change['type']
            ):
                if not is_complete:
                    self.tui.show_streaming_chunk(chunk)
                else:
                    review_dict = review_data
            
            # Finalize this review
            if review_dict:
                self.tui.finalize_streaming_review(review_dict['rating'])
                reviews.append(review_dict)

        # Show summary
        if reviews:
            summary = self.code_reviewer.get_summary(reviews)
            self.tui.show_summary(summary)

    def review_staged(self):
        """Review staged changes."""
        self.tui.show_info("Scanning for staged changes...")

        changes = self.git_handler.get_staged_changes()

        if not changes:
            self.tui.show_warning("No staged changes found.")
            return

        self.tui.show_changes_list(changes)

        if not self.tui.confirm_action(f"\nReview {len(changes)} file(s)?"):
            return

        self.tui.show_info("Starting AI review... Watch the magic happen! ✨")

        reviews = []
        
        # Review each file with streaming output
        for i, change in enumerate(changes, 1):
            self.tui.show_info(f"[{i}/{len(changes)}] Reviewing {change['file']}...")
            self.tui.show_streaming_review_header(
                change['file'],
                change['type'],
                change['language']
            )
            
            # Stream the review
            review_dict = None
            for chunk, is_complete, review_data in self.code_reviewer.review_single_file_streaming(
                change['file'],
                change['diff'],
                change['language'],
                change['type']
            ):
                if not is_complete:
                    self.tui.show_streaming_chunk(chunk)
                else:
                    review_dict = review_data
            
            # Finalize this review
            if review_dict:
                self.tui.finalize_streaming_review(review_dict['rating'])
                reviews.append(review_dict)

        # Show summary
        if reviews:
            summary = self.code_reviewer.get_summary(reviews)
            self.tui.show_summary(summary)

    def run_quick_review(self, staged: bool = False):
        """Run a quick review without interaction.

        Args:
            staged: Review staged changes if True, unstaged if False
        """
        self.tui.show_banner()

        if not self.check_prerequisites():
            return

        self.tui.show_info(f"Reviewing {'staged' if staged else 'unstaged'} changes...")

        reviews = self.code_reviewer.review_changes(staged=staged)

        if not reviews:
            self.tui.show_warning("No changes found.")
            return

        # Show results
        for review in reviews:
            self.tui.show_review_result(review)

        # Show summary
        summary = self.code_reviewer.get_summary(reviews)
        self.tui.show_summary(summary)

    def run_precommit(self, block_on_issues: bool = False) -> int:
        """Run pre-commit review on staged changes with streaming.

        Args:
            block_on_issues: If True, block commit on NEEDS_WORK or ERROR ratings

        Returns:
            Exit code (0 = allow commit, 1 = block commit)
        """
        self.tui.console.print("[bold cyan]🤖 AI Code Review Pre-Commit Hook[/bold cyan]")
        self.tui.console.print()

        # Quick check without banner
        connected = self.ollama_client.check_connection()
        if not connected:
            self.tui.show_warning("Ollama not running. Skipping AI review.")
            self.tui.show_info("Start Ollama with: ollama serve")
            return 0  # Allow commit

        model_available = self.ollama_client.check_model_available()
        if not model_available:
            self.tui.show_warning(f"Model '{config.OLLAMA_MODEL}' not found. Skipping AI review.")
            self.tui.show_info(f"Pull with: ollama pull {config.OLLAMA_MODEL}")
            return 0  # Allow commit

        # Get staged changes
        changes = self.git_handler.get_staged_changes()

        if not changes:
            self.tui.show_info("No staged changes to review.")
            return 0

        self.tui.console.print(f"[cyan]Found {len(changes)} file(s) to review:[/cyan]")
        for change in changes:
            self.tui.console.print(f"  • {change['file']} ({change['language']})")
        self.tui.console.print()

        reviews = []

        # Review each file with streaming
        for i, change in enumerate(changes, 1):
            self.tui.console.print(f"[bold cyan][{i}/{len(changes)}] Reviewing {change['file']}...[/bold cyan]")
            self.tui.show_streaming_review_header(
                change['file'],
                change['type'],
                change['language']
            )

            # Stream the review
            review_dict = None
            for chunk, is_complete, review_data in self.code_reviewer.review_single_file_streaming(
                change['file'],
                change['diff'],
                change['language'],
                change['type']
            ):
                if not is_complete:
                    self.tui.show_streaming_chunk(chunk)
                else:
                    review_dict = review_data

            # Finalize this review
            if review_dict:
                self.tui.finalize_streaming_review(review_dict['rating'])
                reviews.append(review_dict)

        # Show summary
        if reviews:
            summary = self.code_reviewer.get_summary(reviews)
            self.tui.show_summary(summary)

            # Decide whether to block commit
            if block_on_issues:
                needs_work = summary['ratings'].get('NEEDS_WORK', 0)
                errors = summary['errors']

                if needs_work > 0 or errors > 0:
                    self.tui.console.print()
                    self.tui.show_error("Commit blocked due to code quality issues!")
                    self.tui.console.print("[yellow]Fix the issues and try again, or use --no-verify to skip.[/yellow]")
                    return 1  # Block commit

            self.tui.console.print()
            self.tui.show_success("Review complete. Proceeding with commit.")
            return 0

        return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AI Code Review Assistant - Review your code before committing"
    )
    parser.add_argument(
        '--repo-path',
        type=str,
        default=None,
        help='Path to git repository (default: current directory)'
    )
    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Run in interactive mode'
    )
    parser.add_argument(
        '--staged',
        action='store_true',
        help='Review staged changes instead of unstaged'
    )
    parser.add_argument(
        '--precommit',
        action='store_true',
        help='Run in pre-commit hook mode (reviews staged changes with streaming)'
    )
    parser.add_argument(
        '--block-on-issues',
        action='store_true',
        help='Block commit if code has NEEDS_WORK or ERROR ratings (use with --precommit)'
    )

    args = parser.parse_args()

    app = CodeReviewApp(args.repo_path)

    if args.precommit:
        exit_code = app.run_precommit(block_on_issues=args.block_on_issues)
        sys.exit(exit_code)
    elif args.interactive:
        app.run_interactive()
    else:
        app.run_quick_review(staged=args.staged)


if __name__ == "__main__":
    main()

