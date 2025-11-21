.PHONY: help install install-dev test format lint clean build upload run-gui run-example

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install dependencies"
	@echo "  install-dev  Install development dependencies"
	@echo "  test         Run tests"
	@echo "  format       Format code with black"
	@echo "  lint         Run linting with flake8"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build package"
	@echo "  upload       Upload to PyPI (requires credentials)"
	@echo "  run-gui      Run the GUI application"
	@echo "  run-example  Run basic usage example"

# Installation
install:
	pip install -r requirements_gui.txt

install-dev:
	pip install -r requirements_gui.txt
	pip install black flake8 pytest pytest-cov build twine

# Testing
test:
	python -m pytest tests/ -v

test-cov:
	python -m pytest tests/ -v --cov=earthcare_downloader --cov-report=html

# Code quality
format:
	black .

lint:
	flake8 .

check: format lint test

# Build and distribution
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

upload: build
	python -m twine upload dist/*

# Run applications
run-gui:
	python earthcare_downloader_gui.py

run-example:
	python examples/basic_usage.py

# Development helpers
setup-env:
	@echo "Setting up development environment..."
	@echo "Please set the following environment variables:"
	@echo "  export OADS_USERNAME='your_username'"
	@echo "  export OADS_PASSWORD='your_password'"

validate-env:
	@python -c "import os; print('✓ OADS_USERNAME set' if os.getenv('OADS_USERNAME') else '✗ OADS_USERNAME not set')"
	@python -c "import os; print('✓ OADS_PASSWORD set' if os.getenv('OADS_PASSWORD') else '✗ OADS_PASSWORD not set')"