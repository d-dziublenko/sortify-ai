# Contributing to Sortify AI

Thank you for your interest in contributing to Sortify AI! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors. We value diverse perspectives and constructive collaboration.

## Getting Started

To start contributing to Sortify AI, follow these steps:

1. **Fork the Repository**: Click the "Fork" button on the GitHub repository page to create your own copy of the project.

2. **Clone Your Fork**: Clone your forked repository to your local machine:

   ```bash
   git clone https://github.com/d-dziublenko/sortify-ai.git
   cd sortify-ai
   ```

3. **Set Up Development Environment**: Create a virtual environment and install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Create a Feature Branch**: Always work on a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines

### Code Style

We follow Python's PEP 8 style guide with these specific conventions:

- Use 4 spaces for indentation (no tabs)
- Maximum line length of 100 characters
- Use descriptive variable and function names
- Add docstrings to all functions and classes
- Include type hints where appropriate

Example of our coding style:

```python
def analyze_image_batch(
    image_paths: List[str],
    query: str,
    max_workers: int = 4
) -> List[Dict[str, Any]]:
    """
    Analyze a batch of images against a specific query.

    Args:
        image_paths: List of paths to image files
        query: Description to match against images
        max_workers: Number of parallel workers

    Returns:
        List of dictionaries containing analysis results
    """
    # Implementation here
```

### Testing

Before submitting your changes, ensure all tests pass:

```bash
python -m pytest tests/
```

If you add new functionality, please include corresponding tests. We aim for at least 80% code coverage.

### Documentation

Update documentation when you:

- Add new features or functionality
- Change existing behavior
- Add new command-line options
- Modify the API

Documentation includes:

- Docstrings in the code
- README.md updates
- Example scripts if applicable

## Submitting Changes

### Pull Request Process

1. **Commit Your Changes**: Write clear, descriptive commit messages:

   ```bash
   git add .
   git commit -m "Add feature: parallel image processing optimization"
   ```

2. **Push to Your Fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create Pull Request**: Go to the original repository and click "New Pull Request". Select your branch and provide a detailed description of your changes.

### Pull Request Guidelines

Your pull request should:

- Have a clear, descriptive title
- Include a summary of changes
- Reference any related issues
- Include screenshots for UI changes
- Pass all automated tests
- Have no merge conflicts

Example PR description:

```markdown
## Summary

This PR adds support for HEIC image format processing.

## Changes

- Added HEIC to supported formats list
- Integrated pillow-heif library for HEIC decoding
- Updated documentation with new format

## Testing

- Added unit tests for HEIC processing
- Tested with 100+ HEIC images from iPhone

Fixes #123
```

## Types of Contributions

### Bug Reports

When reporting bugs, please include:

- Python version and OS
- Steps to reproduce the issue
- Expected vs actual behavior
- Error messages or logs
- Sample images if relevant (ensure no private data)

### Feature Requests

For new features, please:

- Explain the use case
- Describe the desired behavior
- Provide examples if possible
- Consider backward compatibility

### Code Contributions

We welcome various types of code contributions:

- Performance improvements
- New categorization algorithms
- Additional export formats
- UI enhancements
- Bug fixes
- Test coverage improvements

### Documentation

Help improve our documentation by:

- Fixing typos or unclear explanations
- Adding more examples
- Creating tutorials
- Translating documentation

## Development Setup for Advanced Features

### Running with Development Mode

For development, you can run the analyzer with additional debugging:

```python
# In your development script
import logging
logging.basicConfig(level=logging.DEBUG)

from image_analyzer import ImageAnalyzer
analyzer = ImageAnalyzer(api_key="your-key", debug=True)
```

### Testing with Mock API

To avoid using API credits during development, use our mock mode:

```bash
MOCK_API=true python image_analyzer.py -f ./test_images -q "test query"
```

## Questions or Need Help?

If you have questions or need help with your contribution:

- Check existing issues and discussions
- Create a new issue with the "question" label
- Reach out to maintainers

Thank you for contributing to Sortify AI! Your efforts help make image organization smarter and more accessible for everyone.
