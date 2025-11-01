"""Core code review logic."""

from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from git_handler import GitHandler
from ollama_client import OllamaClient
import config


class CodeReviewer:
    """Main code reviewer orchestrator."""

    def __init__(self, git_handler: GitHandler, ollama_client: OllamaClient):
        """Initialize code reviewer.

        Args:
            git_handler: Git operations handler
            ollama_client: Ollama AI client
        """
        self.git_handler = git_handler
        self.ollama_client = ollama_client

    def review_changes(self, staged: bool = False) -> List[Dict[str, any]]:
        """Review all changes (staged or unstaged).

        Args:
            staged: Whether to review staged changes (True) or unstaged (False)

        Returns:
            List of review results
        """
        if staged:
            changes = self.git_handler.get_staged_changes()
        else:
            changes = self.git_handler.get_unstaged_changes()

        if not changes:
            return []

        reviews = []

        # Review files in batches
        for i in range(0, len(changes), config.REVIEW_BATCH_SIZE):
            batch = changes[i:i + config.REVIEW_BATCH_SIZE]
            batch_reviews = self._review_batch(batch)
            reviews.extend(batch_reviews)

        return reviews

    def _review_batch(self, changes: List[Dict[str, str]]) -> List[Dict[str, any]]:
        """Review a batch of changes in parallel.

        Args:
            changes: List of changes to review

        Returns:
            List of review results
        """
        reviews = []

        with ThreadPoolExecutor(max_workers=config.REVIEW_BATCH_SIZE) as executor:
            future_to_change = {
                executor.submit(
                    self._review_single_file,
                    change['file'],
                    change['diff'],
                    change['language'],
                    change['type']
                ): change for change in changes
            }

            for future in as_completed(future_to_change):
                change = future_to_change[future]
                try:
                    review = future.result()
                    reviews.append(review)
                except Exception as e:
                    reviews.append({
                        'file': change['file'],
                        'type': change['type'],
                        'language': change['language'],
                        'review': f"Error during review: {str(e)}",
                        'rating': 'ERROR',
                        'error': True
                    })

        return reviews

    def _review_single_file(self, filename: str, diff: str, language: str, change_type: str) -> Dict[str, any]:
        """Review a single file.

        Args:
            filename: Name of the file
            diff: The diff or content
            language: Programming language
            change_type: Type of change (modified, staged, untracked)

        Returns:
            Review result dict
        """
        review_text = self.ollama_client.review_code(filename, diff, language)
        rating = self._extract_rating(review_text)

        return {
            'file': filename,
            'type': change_type,
            'language': language,
            'review': review_text,
            'rating': rating,
            'diff_lines': len(diff.split('\n')),
            'error': False
        }

    def review_single_file_streaming(self, filename: str, diff: str, language: str, change_type: str):
        """Review a single file with streaming output.

        Args:
            filename: Name of the file
            diff: The diff or content
            language: Programming language
            change_type: Type of change (modified, staged, untracked)

        Yields:
            Tuples of (chunk_text, is_complete, review_dict)
            - chunk_text: The text chunk from the AI
            - is_complete: True if this is the final chunk
            - review_dict: Complete review dict (only on final chunk)
        """
        review_text = ""
        try:
            for chunk in self.ollama_client.review_code_streaming(filename, diff, language):
                review_text += chunk
                yield (chunk, False, None)

            # Final chunk with complete review
            rating = self._extract_rating(review_text)
            review_dict = {
                'file': filename,
                'type': change_type,
                'language': language,
                'review': review_text,
                'rating': rating,
                'diff_lines': len(diff.split('\n')),
                'error': False
            }
            yield ("", True, review_dict)
        except Exception as e:
            error_msg = f"Error during review: {str(e)}"
            review_dict = {
                'file': filename,
                'type': change_type,
                'language': language,
                'review': error_msg,
                'rating': 'ERROR',
                'error': True
            }
            yield (error_msg, True, review_dict)

    def _extract_rating(self, review_text: str) -> str:
        """Extract rating from review text.

        Args:
            review_text: The AI's review text

        Returns:
            Rating string
        """
        review_upper = review_text.upper()

        ratings = ['EXCELLENT', 'GOOD', 'FAIR', 'NEEDS_WORK', 'ERROR']
        for rating in ratings:
            if rating in review_upper:
                return rating

        return 'UNKNOWN'

    def get_summary(self, reviews: List[Dict[str, any]]) -> Dict[str, any]:
        """Generate a summary of all reviews.

        Args:
            reviews: List of review results

        Returns:
            Summary dict
        """
        total = len(reviews)
        errors = sum(1 for r in reviews if r.get('error', False))

        ratings = {}
        for review in reviews:
            rating = review.get('rating', 'UNKNOWN')
            ratings[rating] = ratings.get(rating, 0) + 1

        # Calculate overall assessment
        excellent = ratings.get('EXCELLENT', 0)
        good = ratings.get('GOOD', 0)
        fair = ratings.get('FAIR', 0)
        needs_work = ratings.get('NEEDS_WORK', 0)

        if excellent >= total * 0.7:
            overall = 'EXCELLENT'
        elif (excellent + good) >= total * 0.7:
            overall = 'GOOD'
        elif needs_work >= total * 0.3:
            overall = 'NEEDS_WORK'
        else:
            overall = 'FAIR'

        return {
            'total_files': total,
            'errors': errors,
            'ratings': ratings,
            'overall': overall,
            'reviews': reviews
        }

