"""Ollama client for AI code reviews."""

import ollama
from typing import Optional
import config


class OllamaClient:
    """Client for interacting with Ollama API."""

    def __init__(self, model: str = config.OLLAMA_MODEL, host: str = config.OLLAMA_HOST):
        """Initialize the Ollama client.

        Args:
            model: The model to use (default: llama3.2:1b)
            host: The Ollama host URL
        """
        self.model = model
        self.host = host
        self.client = ollama.Client(host=host)

    def check_connection(self) -> bool:
        """Check if Ollama is running and accessible.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            self.client.list()
            return True
        except Exception:
            return False

    def check_model_available(self) -> bool:
        """Check if the configured model is available.

        Returns:
            True if model is available, False otherwise
        """
        try:
            models = self.client.list()
            return any(self.model in model['name'] for model in models.get('models', []))
        except Exception:
            return False

    def review_code(self, filename: str, diff: str, language: str = "python") -> Optional[str]:
        """Request a code review from the AI model.

        Args:
            filename: Name of the file being reviewed
            diff: The code diff to review
            language: Programming language of the code

        Returns:
            The AI's review response, or None if there was an error
        """
        if len(diff) > config.MAX_DIFF_SIZE:
            diff = diff[:config.MAX_DIFF_SIZE] + "\n... (truncated)"

        prompt = config.REVIEW_PROMPT_TEMPLATE.format(
            filename=filename,
            language=language,
            diff=diff
        )

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': config.SYSTEM_PROMPT
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.3,
                    'num_predict': 500,
                }
            )

            return response['message']['content']
        except Exception as e:
            return f"Error during review: {str(e)}"

    def get_quick_summary(self, changes_summary: str) -> Optional[str]:
        """Get a quick summary of all changes.

        Args:
            changes_summary: Summary of all changes

        Returns:
            Quick summary from AI
        """
        prompt = f"""Provide a brief overview (2-3 sentences) of these code changes:

{changes_summary}

Focus on the overall impact and any critical concerns."""

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'system',
                        'content': 'You are a code reviewer providing concise summaries.'
                    },
                    {
                        'role': 'user',
                        'content': prompt
                    }
                ],
                options={
                    'temperature': 0.3,
                    'num_predict': 150,
                }
            )

            return response['message']['content']
        except Exception as e:
            return f"Error generating summary: {str(e)}"

