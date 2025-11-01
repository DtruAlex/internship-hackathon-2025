"""Main entry point for the AI Code Review Assistant."""

import sys
import argparse
from git_handler import GitHandler
from ollama_client import OllamaClient
from code_reviewer import CodeReviewer
from tui import ReviewTUI
import config


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

        self.tui.show_info("Starting AI review... This may take a moment.")

        progress = self.tui.show_review_progress(len(changes))

        with progress:
            task = progress.add_task("[cyan]Reviewing files...", total=len(changes))

            reviews = []
            for i in range(0, len(changes), config.REVIEW_BATCH_SIZE):
                batch = changes[i:i + config.REVIEW_BATCH_SIZE]
                batch_reviews = self.code_reviewer._review_batch(batch)
                reviews.extend(batch_reviews)
                progress.update(task, advance=len(batch))

        # Show results
        self.tui.console.print()
        for review in reviews:
            self.tui.show_review_result(review)

        # Show summary
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

        self.tui.show_info("Starting AI review... This may take a moment.")

        progress = self.tui.show_review_progress(len(changes))

        with progress:
            task = progress.add_task("[cyan]Reviewing files...", total=len(changes))

            reviews = []
            for i in range(0, len(changes), config.REVIEW_BATCH_SIZE):
                batch = changes[i:i + config.REVIEW_BATCH_SIZE]
                batch_reviews = self.code_reviewer._review_batch(batch)
                reviews.extend(batch_reviews)
                progress.update(task, advance=len(batch))

        # Show results
        self.tui.console.print()
        for review in reviews:
            self.tui.show_review_result(review)

        # Show summary
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

    args = parser.parse_args()

    app = CodeReviewApp(args.repo_path)

    if args.interactive:
        app.run_interactive()
    else:
        app.run_quick_review(staged=args.staged)


if __name__ == "__main__":
    main()

