# Contributing to Gesture AI Agent

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing Requirements](#testing-requirements)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

We are committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites
- Python 3.9 or higher
- Git
- pip (Python package manager)

### Fork and Clone
```bash
# Fork the repository on GitHub
# Clone your fork
git clone https://github.com/yourusername/gesture-ai-agent.git
cd gesture-ai-agent
```

## Development Setup

### 1. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
# Install development dependencies
pip install -e ".[dev]"

# Or using requirements
pip install -r requirements-prod.txt
```

### 3. Setup Pre-commit Hooks
```bash
pre-commit install
```

## Code Style

We follow PEP 8 with the following additional standards:

### Type Hints
All functions must include type hints:

```python
# Good
def process_gesture(gesture_data: dict) -> dict:
    """Process gesture and return result."""
    pass

# Bad
def process_gesture(gesture_data):
    pass
```

### Docstrings
Use Google-style docstrings:

```python
def detect_emotion(frame: np.ndarray) -> dict:
    """Detect emotion from image frame.
    
    Args:
        frame: Input image frame as numpy array
        
    Returns:
        Dictionary containing emotion and confidence:
        {
            'emotion': str,
            'confidence': float,
            'landmarks': list
        }
        
    Raises:
        ValueError: If frame is invalid
    """
    pass
```

### Code Formatting

Use these tools to maintain code quality:

```bash
# Format code with black
black .

# Sort imports with isort
isort .

# Check code style with flake8
flake8 .

# Type checking with mypy
mypy .

# lint with pylint
pylint *.py
```

### Naming Conventions
- Functions: `lowercase_with_underscores`
- Classes: `PascalCase`
- Constants: `UPPERCASE_WITH_UNDERSCORES`
- Private methods: `_leading_underscore`

### Comments
```python
# Good: Explains why, not what
# Use temporal smoothing to prevent gesture jitter from sensor noise
gesture = self._smooth_gesture(gesture)

# Bad: Obvious from code
# Add 5 to x
x = x + 5
```

## Testing Requirements

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/unit/test_gesture_processor.py

# Run with verbose output
pytest -v
```

### Writing Tests
All new features must include tests. Follow these patterns:

```python
import pytest
from gesture_processor import GestureProcessor

class TestGestureProcessor:
    """Test cases for GestureProcessor class."""
    
    @pytest.fixture
    def processor(self):
        """Create processor instance for testing."""
        return GestureProcessor()
    
    def test_analyze_thumbs_up(self, processor):
        """Test thumbs up gesture recognition."""
        gesture_data = {
            'hands': mock_hand_data(),
            'pose': None
        }
        result = processor.analyze_gesture(gesture_data)
        
        assert result['gesture_type'] == 'thumbs_up'
        assert result['confidence'] > 0.7
    
    def test_invalid_input_raises_error(self, processor):
        """Test that invalid input raises appropriate error."""
        with pytest.raises(ValueError):
            processor.analyze_gesture({})
```

### Test Coverage
- Aim for >80% code coverage
- Include unit, integration, and system tests
- Test error conditions and edge cases

## Commit Guidelines

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test additions/modifications
- `chore`: Build, dependencies, etc.

### Examples
```
feat(gesture): add support for custom gesture detection
fix(voice): resolve microphone initialization timeout issue
docs(api): update API reference for new methods
test(facial): improve emotion detection test coverage
```

### Commit Best Practices
- Keep commits focused and atomic
- Use present tense ("add feature" not "added feature")
- Reference issues: "Fixes #123"
- Write meaningful commit messages

## Pull Request Process

### Before Submitting
1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make your changes
3. Run tests: `pytest`
4. Format code: `black . && isort .`
5. Check style: `flake8 . && mypy .`
6. Test coverage: `pytest --cov=.`

### Submitting PR
1. Push to your fork
2. Create Pull Request with clear description
3. Link related issues
4. Ensure CI/CD passes
5. Request review from maintainers

### PR Description Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring

## Related Issues
Fixes #issue_number

## Testing
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] All tests passing
- [ ] Coverage maintained >80%

## Changes Made
- Change 1
- Change 2

## Screenshots (if applicable)
```

## Reporting Issues

### Bug Report Template
```markdown
## Description
Brief description of the bug

## Reproduction
Steps to reproduce:
1. ...
2. ...
3. ...

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [Windows/Linux/Mac]
- Python: [3.9/3.10/3.11]
- Version: [version number]

## Logs/Error Messages
```

### Feature Request Template
```markdown
## Description
Clear description of desired feature

## Use Case
Why this feature is needed

## Proposed Solution
How it could be implemented

## Alternative Solutions
Other approaches considered
```

## Development Workflow

### 1. Identify Issue
Look through open issues or create a new one

### 2. Create Branch
```bash
git checkout -b feature/issue-number-description
git push -u origin feature/issue-number-description
```

### 3. Implement Changes
- Follow code style guidelines
- Write tests as you go
- Add docstrings and comments

### 4. Test Locally
```bash
pytest --cov=.
black . && isort .
flake8 . && mypy .
```

### 5. Commit and Push
```bash
git add .
git commit -m "feat(scope): clear commit message"
git push
```

### 6. Create Pull Request
- Link related issues
- Describe changes clearly
- Request review

## Resources

- [API Reference](API_REFERENCE.md)
- [Architecture Guide](ARCHITECTURE.md)
- [Testing Guide](TESTING.md)
- [Code Style Guide](https://pep8.org/)

## Questions?

If you have questions about contributing:
1. Check existing documentation
2. Search closed issues and discussions
3. Create a discussion or ask in issues

Thank you for contributing!
