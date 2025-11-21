# Contributing to EarthCARE Downloader

Thank you for your interest in contributing to EarthCARE Downloader! This document provides guidelines and information for contributors.

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker to report bugs
- Provide a clear description of the problem
- Include steps to reproduce the issue
- Specify your operating system and Python version
- Include any relevant error messages or logs

### Suggesting Features

- Open an issue with the label "enhancement"
- Describe the feature and its use case
- Explain why it would be beneficial
- Consider providing a basic implementation idea

### Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature-name`)
3. Make your changes
4. Add or update tests as needed
5. Update documentation if necessary
6. Commit your changes with clear messages
7. Push to your fork
8. Submit a pull request

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git

### Setting up the Development Environment

```bash
# Clone your fork
git clone https://github.com/your-username/earthcare_downloader.git
cd earthcare_downloader

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install black flake8 pytest pytest-cov
```

## Code Style

### Python Code Style

We use [Black](https://black.readthedocs.io/) for code formatting and [Flake8](https://flake8.pycqa.org/) for linting.

```bash
# Format code
black .

# Check linting
flake8 .
```

### Code Standards

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and small
- Add type hints where appropriate

### Commit Message Format

Use clear, descriptive commit messages:

```type(scope): description

[optional body]

[optional footer]
```

Examples:

- `feat(downloader): add support for new product types`
- `fix(gui): resolve progress bar update issue`
- `docs(readme): update installation instructions`

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=earthcare_downloader

# Run specific test file
pytest tests/test_downloader.py
```

### Writing Tests

- Write tests for new features
- Update existing tests when modifying functionality
- Ensure good test coverage
- Use descriptive test names

## Documentation

### Updating Documentation

- Update the README.md for user-facing changes
- Update docstrings for API changes
- Update CHANGELOG.md for notable changes
- Add examples for new features

### Documentation Style

- Use clear, concise language
- Provide examples where helpful
- Keep documentation up to date with code changes

## Pull Request Guidelines

### Before Submitting

- Ensure all tests pass
- Update documentation as needed
- Update CHANGELOG.md
- Rebase your branch on the latest main branch
- Squash commits if appropriate

### Pull Request Description

Include:

- Clear description of the changes
- Link to related issues
- Screenshots for GUI changes
- Testing instructions
- Breaking changes (if any)

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on what is best for the community

### Getting Help

- Check existing issues and documentation first
- Ask questions in GitHub issues or discussions
- Be specific about your problem or question
- Provide relevant context and details

## Recognition

Contributors will be acknowledged in:

- GitHub contributors list
- CHANGELOG.md for significant contributions
- README.md acknowledgments section

## License

By contributing to EarthCARE Downloader, you agree that your contributions will be licensed under the same license as the project (MIT License).

Thank you for contributing to EarthCARE Downloader!
