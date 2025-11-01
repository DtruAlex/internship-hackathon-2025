"""Git operations handler for the code review assistant."""

import git
from pathlib import Path
from typing import List, Dict, Optional
from . import config


class GitHandler:
    """Handle Git operations for code review."""

    def __init__(self, repo_path: Optional[str] = None):
        """Initialize Git handler.

        Args:
            repo_path: Path to git repository (default: current directory)
        """
        try:
            self.repo = git.Repo(repo_path or '.', search_parent_directories=True)
            self.repo_root = self.repo.working_tree_dir
        except git.InvalidGitRepositoryError:
            raise ValueError("Not a git repository. Please run from within a git repository.")

    def get_unstaged_changes(self) -> List[Dict[str, str]]:
        """Get all unstaged changes.

        Returns:
            List of dicts with file info and diffs
        """
        changes = []

        # Get modified files
        modified_files = [item.a_path for item in self.repo.index.diff(None)]

        # Get untracked files
        untracked_files = self.repo.untracked_files

        for filepath in modified_files:
            if self._should_exclude(filepath):
                continue

            try:
                # Try to get diff against HEAD, fall back to full file if no commits
                try:
                    diff = self.repo.git.diff('HEAD', filepath)
                except:
                    diff = self.repo.git.diff(filepath)

                if diff:
                    changes.append({
                        'file': filepath,
                        'type': 'modified',
                        'diff': diff,
                        'language': self._detect_language(filepath)
                    })
            except Exception as e:
                changes.append({
                    'file': filepath,
                    'type': 'modified',
                    'diff': f"Error getting diff: {str(e)}",
                    'language': self._detect_language(filepath)
                })

        for filepath in untracked_files:
            if self._should_exclude(filepath):
                continue

            try:
                full_path = Path(self.repo_root) / filepath
                if full_path.stat().st_size > config.MAX_FILE_SIZE:
                    continue

                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()

                changes.append({
                    'file': filepath,
                    'type': 'untracked',
                    'diff': content,
                    'language': self._detect_language(filepath)
                })
            except Exception:
                continue

        return changes

    def get_staged_changes(self) -> List[Dict[str, str]]:
        """Get all staged changes.

        Returns:
            List of dicts with file info and diffs
        """
        changes = []

        try:
            # Try to get staged files (requires at least one commit)
            staged_files = [item.a_path for item in self.repo.index.diff('HEAD')]
        except:
            # No commits yet, get all files in index
            staged_files = [entry[0] for entry in self.repo.index.entries.keys()]

        for filepath in staged_files:
            if self._should_exclude(filepath):
                continue

            diff = None
            try:
                try:
                    diff = self.repo.git.diff('HEAD', filepath, cached=True)
                except:
                    # No HEAD yet, show the full staged file
                    full_path = Path(self.repo_root) / filepath
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        diff = f.read()

                if diff:
                    changes.append({
                        'file': filepath,
                        'type': 'staged',
                        'diff': diff,
                        'language': self._detect_language(filepath)
                    })
            except Exception as e:
                changes.append({
                    'file': filepath,
                    'type': 'staged',
                    'diff': f"Error getting diff: {str(e)}",
                    'language': self._detect_language(filepath)
                })

        return changes

    def get_file_diff(self, filepath: str, staged: bool = False) -> Optional[str]:
        """Get diff for a specific file.

        Args:
            filepath: Path to the file
            staged: Whether to get staged or unstaged diff

        Returns:
            Diff string or None
        """
        try:
            if staged:
                return self.repo.git.diff('HEAD', filepath, cached=True)
            else:
                return self.repo.git.diff('HEAD', filepath)
        except Exception:
            return None

    def _should_exclude(self, filepath: str) -> bool:
        """Check if file should be excluded from review.

        Args:
            filepath: Path to check

        Returns:
            True if should be excluded
        """
        from fnmatch import fnmatch
        return any(fnmatch(filepath, pattern) for pattern in config.EXCLUDE_PATTERNS)

    def _detect_language(self, filepath: str) -> str:
        """Detect programming language from file extension.

        Args:
            filepath: Path to the file

        Returns:
            Language name
        """
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.jsx': 'jsx',
            '.tsx': 'tsx',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.h': 'c',
            '.hpp': 'cpp',
            '.cs': 'csharp',
            '.go': 'go',
            '.rs': 'rust',
            '.rb': 'ruby',
            '.php': 'php',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.sh': 'bash',
            '.bash': 'bash',
            '.zsh': 'zsh',
            '.fish': 'fish',
            '.yaml': 'yaml',
            '.yml': 'yaml',
            '.json': 'json',
            '.xml': 'xml',
            '.html': 'html',
            '.css': 'css',
            '.scss': 'scss',
            '.sql': 'sql',
            '.md': 'markdown',
            '.txt': 'text'
        }

        ext = Path(filepath).suffix.lower()
        return ext_map.get(ext, 'text')

    def get_repo_status(self) -> Dict[str, any]:
        """Get current repository status.

        Returns:
            Dict with repo status info
        """
        try:
            branch_name = self.repo.active_branch.name
        except:
            branch_name = "HEAD (no commits yet)"

        try:
            # Try to get staged count (requires at least one commit)
            staged_count = len([item for item in self.repo.index.diff('HEAD')])
        except:
            # No commits yet, count staged files differently
            staged_count = len(self.repo.index.entries)

        return {
            'branch': branch_name,
            'is_dirty': self.repo.is_dirty(),
            'untracked_count': len(self.repo.untracked_files),
            'modified_count': len([item for item in self.repo.index.diff(None)]),
            'staged_count': staged_count
        }

