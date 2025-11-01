"""Rich TUI interface for the code review assistant."""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.markdown import Markdown
from rich.prompt import Prompt, Confirm
from rich import box
from rich.text import Text
from typing import List, Dict


class ReviewTUI:
    """Terminal User Interface for code reviews."""

    def __init__(self):
        """Initialize the TUI."""
        self.console = Console()

    def show_banner(self):
        """Display welcome banner."""
        banner = """
    ╔═══════════════════════════════════════════════╗
    ║   🤖 AI Code Review Assistant                ║
    ║   Powered by Ollama + LLama 3.2:1B          ║
    ╚═══════════════════════════════════════════════╝
        """
        self.console.print(banner, style="bold cyan")

    def show_repo_status(self, status: Dict[str, any]):
        """Display repository status.

        Args:
            status: Repository status dict
        """
        table = Table(show_header=False, box=box.ROUNDED, padding=(0, 1))
        table.add_column("Property", style="cyan")
        table.add_column("Value", style="yellow")

        table.add_row("📁 Branch", status['branch'])
        table.add_row("📝 Modified", str(status['modified_count']))
        table.add_row("✅ Staged", str(status['staged_count']))
        table.add_row("➕ Untracked", str(status['untracked_count']))
        table.add_row("🔄 Dirty", "Yes" if status['is_dirty'] else "No")

        self.console.print(Panel(table, title="Repository Status", border_style="blue"))

    def show_connection_status(self, connected: bool, model_available: bool):
        """Show Ollama connection status.

        Args:
            connected: Whether Ollama is connected
            model_available: Whether the model is available
        """
        if connected and model_available:
            self.console.print("✅ Ollama connected - Model ready", style="bold green")
        elif connected:
            self.console.print("⚠️  Ollama connected - Model not found. Run: ollama pull llama3.2:1b",
                             style="bold yellow")
        else:
            self.console.print("❌ Ollama not connected. Make sure it's running: ollama serve",
                             style="bold red")

    def show_changes_list(self, changes: List[Dict[str, str]]):
        """Display list of changes to be reviewed.

        Args:
            changes: List of changes
        """
        if not changes:
            self.console.print("No changes to review!", style="yellow")
            return

        table = Table(title="Changes to Review", box=box.ROUNDED)
        table.add_column("File", style="cyan", no_wrap=False)
        table.add_column("Type", style="magenta")
        table.add_column("Language", style="green")
        table.add_column("Lines", justify="right", style="yellow")

        for change in changes:
            change_type = change['type'].upper()
            lines = str(len(change['diff'].split('\n')))

            # Add emoji based on type
            type_emoji = {
                'MODIFIED': '📝',
                'STAGED': '✅',
                'UNTRACKED': '➕'
            }
            emoji = type_emoji.get(change_type, '📄')

            table.add_row(
                change['file'],
                f"{emoji} {change_type}",
                change['language'],
                lines
            )

        self.console.print(table)

    def show_review_progress(self, total: int) -> Progress:
        """Create and return a progress bar for reviews.

        Args:
            total: Total number of files to review

        Returns:
            Progress object
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=self.console
        )
        return progress

    def show_review_result(self, review: Dict[str, any], show_diff: bool = False):
        """Display a single review result.

        Args:
            review: Review result dict
            show_diff: Whether to show the diff
        """
        # Rating color
        rating_colors = {
            'EXCELLENT': 'bold green',
            'GOOD': 'green',
            'FAIR': 'yellow',
            'NEEDS_WORK': 'red',
            'ERROR': 'bold red',
            'UNKNOWN': 'white'
        }

        rating = review.get('rating', 'UNKNOWN')
        color = rating_colors.get(rating, 'white')

        # Create header
        header = Text()
        header.append(f"📄 {review['file']}", style="bold cyan")
        header.append(f" [{review['type']}]", style="dim")
        header.append(f" • {review['language']}", style="green")
        header.append(f" • Rating: {rating}", style=color)

        self.console.print()
        self.console.print(header)
        self.console.print("─" * self.console.width, style="dim")

        # Show review
        if review.get('error'):
            self.console.print(review['review'], style="red")
        else:
            # Try to format as markdown
            try:
                md = Markdown(review['review'])
                self.console.print(md)
            except:
                self.console.print(review['review'])

        self.console.print()

    def show_streaming_review_header(self, filename: str, change_type: str, language: str):
        """Display the header for a streaming review.

        Args:
            filename: Name of the file being reviewed
            change_type: Type of change
            language: Programming language
        """
        header = Text()
        header.append(f"📄 {filename}", style="bold cyan")
        header.append(f" [{change_type}]", style="dim")
        header.append(f" • {language}", style="green")
        header.append(" • Reviewing...", style="yellow")

        self.console.print()
        self.console.print(header)
        self.console.print("─" * self.console.width, style="dim")

    def show_streaming_chunk(self, chunk: str):
        """Display a chunk of streaming review.

        Args:
            chunk: Text chunk to display
        """
        self.console.print(chunk, end="")

    def finalize_streaming_review(self, rating: str):
        """Display the final rating after streaming is complete.

        Args:
            rating: Final rating
        """
        rating_colors = {
            'EXCELLENT': 'bold green',
            'GOOD': 'green',
            'FAIR': 'yellow',
            'NEEDS_WORK': 'red',
            'ERROR': 'bold red',
            'UNKNOWN': 'white'
        }
        color = rating_colors.get(rating, 'white')
        self.console.print(f"\n\n[{color}]✓ Rating: {rating}[/{color}]")
        self.console.print()

    def show_summary(self, summary: Dict[str, any]):
        """Display review summary.

        Args:
            summary: Summary dict
        """
        # Overall status
        overall = summary['overall']
        overall_colors = {
            'EXCELLENT': 'bold green',
            'GOOD': 'green',
            'FAIR': 'yellow',
            'NEEDS_WORK': 'red'
        }
        color = overall_colors.get(overall, 'white')

        # Create summary panel
        summary_text = f"""
[bold]Overall Assessment:[/bold] [{color}]{overall}[/{color}]

[bold]Files Reviewed:[/bold] {summary['total_files']}
[bold]Errors:[/bold] {summary['errors']}

[bold]Rating Distribution:[/bold]
"""

        for rating, count in summary['ratings'].items():
            if rating != 'UNKNOWN' and count > 0:
                percentage = (count / summary['total_files']) * 100
                summary_text += f"  • {rating}: {count} ({percentage:.1f}%)\n"

        self.console.print(Panel(summary_text, title="📊 Review Summary", border_style="blue", box=box.DOUBLE))

    def show_menu(self) -> str:
        """Show main menu and get user choice.

        Returns:
            User's choice
        """
        self.console.print("\n[bold cyan]What would you like to do?[/bold cyan]")
        self.console.print("  1. Review unstaged changes")
        self.console.print("  2. Review staged changes")
        self.console.print("  3. Show repository status")
        self.console.print("  4. Exit")

        choice = Prompt.ask("\nEnter your choice", choices=["1", "2", "3", "4"], default="1")
        return choice

    def confirm_action(self, message: str) -> bool:
        """Ask for user confirmation.

        Args:
            message: Confirmation message

        Returns:
            True if confirmed
        """
        return Confirm.ask(message)

    def show_error(self, message: str):
        """Display an error message.

        Args:
            message: Error message
        """
        self.console.print(f"\n❌ Error: {message}", style="bold red")

    def show_success(self, message: str):
        """Display a success message.

        Args:
            message: Success message
        """
        self.console.print(f"\n✅ {message}", style="bold green")

    def show_info(self, message: str):
        """Display an info message.

        Args:
            message: Info message
        """
        self.console.print(f"\nℹ️  {message}", style="bold blue")

    def show_warning(self, message: str):
        """Display a warning message.

        Args:
            message: Warning message
        """
        self.console.print(f"\n⚠️  {message}", style="bold yellow")

    def clear(self):
        """Clear the console."""
        self.console.clear()

    def pause(self):
        """Wait for user to press enter."""
        self.console.input("\n[dim]Press Enter to continue...[/dim]")

