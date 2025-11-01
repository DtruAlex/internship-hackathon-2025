.PHONY: help install dev-install test clean run install-hook demo check-status

help:
	@echo "AI Code Review Assistant - Available commands:"
	@echo ""
	@echo "  make install        - Install the package"
	@echo "  make dev-install    - Install in development mode"
	@echo "  make test           - Run tests"
	@echo "  make clean          - Clean build artifacts"
	@echo "  make run            - Run in interactive mode"
	@echo "  make install-hook   - Install pre-commit hook"
	@echo "  make demo           - Run demo"
	@echo "  make check-status   - Check system status"
	@echo ""

install:
	pip install -r requirements.txt

dev-install:
	pip install -e .

test:
	@echo "Running tests..."
	python -m pytest tests/ -v

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

run:
	./ai-code-review --interactive

install-hook:
	./scripts/install-hook.sh

demo:
	./scripts/demo-precommit.sh

check-status:
	./scripts/check-status.sh

