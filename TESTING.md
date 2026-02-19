# Testing Guide - Gesture AI Agent

Comprehensive guide for running, writing, and maintaining tests in the Gesture AI Agent project.

## Table of Contents
1. [Quick Start](#quick-start)
2. [Test Structure](#test-structure)
3. [Running Tests](#running-tests)
4. [Writing Tests](#writing-tests)
5. [Test Fixtures](#test-fixtures)
6. [Mocking](#mocking)
7. [Coverage](#coverage)
8. [CI/CD Integration](#cicd-integration)

## Quick Start

### Installation
```bash
# Install test dependencies
pip install pytest pytest-cov pytest-mock

# Or install with development extras
pip install -e ".[dev]"
```

### Run All Tests
```bash
pytest
```

### Run with Coverage
```bash
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

## Test Structure

### Directory Layout
```
tests/
├── __init__.py
├── unit/
│   ├── test_gesture_processor.py
│   ├── test_facial_detector.py
│   ├── test_action_executor.py
│   ├── test_voice_commander.py
│   ├── test_conversation_engine.py
│   ├── test_config.py
│   └── test_logger.py
├── integration/
│   ├── test_gesture_to_action.py
│   ├── test_mood_to_action.py
│   ├── test_voice_to_action.py
│   └── test_end_to_end.py
└── fixtures/
    ├── __init__.py
    ├── camera_data.py
    ├── gesture_data.py
    ├── facial_data.py
    └── mock_config.py
```

### Test Naming Convention
- Test files: `test_*.py` or `*_test.py`
- Test classes: `Test<ModuleName>`
- Test methods: `test_<functionality>`

Example:
```python
# Filename: test_gesture_processor.py

class TestGestureProcessor:
    def test_detect_thumbs_up(self):
        pass
    
    def test_detect_peace_sign(self):
        pass
```

## Running Tests

### Basic Commands
```bash
# Run all tests
pytest

# Run specific file
pytest tests/unit/test_gesture_processor.py

# Run specific test
pytest tests/unit/test_gesture_processor.py::TestGestureProcessor::test_detect_thumbs_up

# Run with pattern matching
pytest -k "thumbs_up"

# Run tests with verbose output
pytest -v

# Run with print statements visible
pytest -s

# Stop on first failure
pytest -x

# Show slowest tests
pytest --durations=10
```

### Coverage Reports
```bash
# Generate terminal report
pytest --cov=. --cov-report=term-missing

# Generate HTML report
pytest --cov=. --cov-report=html
open htmlcov/index.html

# Generate XML report (for CI/CD)
pytest --cov=. --cov-report=xml

# Check coverage for specific module
pytest --cov=gesture_processor --cov-report=term-missing
```

### Parallel Testing
```bash
# Run tests in parallel (install pytest-xdist first)
pip install pytest-xdist
pytest -n auto
```

## Writing Tests

### Basic Test
```python
import pytest
from gesture_processor import GestureProcessor

class TestGestureProcessor:
    def test_analyze_gesture_returns_dict(self):
        """Test that analyze_gesture returns a dictionary."""
        processor = GestureProcessor()
        result = processor.analyze_gesture({})
        
        assert isinstance(result, dict)
        assert 'gesture_type' in result
        assert 'confidence' in result
```

### Test with Fixtures
```python
import pytest
from gesture_processor import GestureProcessor

class TestGestureProcessor:
    @pytest.fixture
    def processor(self):
        """Create a GestureProcessor instance."""
        return GestureProcessor()
    
    def test_analyze_gesture(self, processor):
        """Test gesture analysis with fixture."""
        result = processor.analyze_gesture({})
        assert result is not None
```

### Parameterized Tests
```python
import pytest
from gesture_processor import GestureProcessor

class TestGestureDetection:
    @pytest.mark.parametrize("gesture_type,expected_confidence", [
        ("thumbs_up", 0.92),
        ("peace_sign", 0.88),
        ("open_palm", 0.85),
    ])
    def test_gesture_confidence(self, gesture_type, expected_confidence):
        """Test gesture detection confidence."""
        # Test implementation
        pass
```

### Testing Exceptions
```python
import pytest
from gesture_processor import GestureProcessor

class TestGestureProcessor:
    def test_invalid_input_raises_error(self):
        """Test that invalid input raises ValueError."""
        processor = GestureProcessor()
        
        with pytest.raises(ValueError):
            processor.analyze_gesture(None)
    
    def test_specific_error_message(self):
        """Test specific error message."""
        processor = GestureProcessor()
        
        with pytest.raises(ValueError, match="Invalid gesture data"):
            processor.analyze_gesture({})
```

### Testing with Multiple Assertions
```python
import pytest
from gesture_processor import GestureProcessor

class TestGestureProcessor:
    def test_analyze_gesture_complete(self):
        """Test complete gesture analysis."""
        processor = GestureProcessor()
        result = processor.analyze_gesture({})
        
        # Test all expected fields
        assert 'gesture_type' in result
        assert 'confidence' in result
        assert 'details' in result
        assert 'facial_data' in result
        
        # Test value types
        assert isinstance(result['gesture_type'], str)
        assert isinstance(result['confidence'], float)
        assert 0.0 <= result['confidence'] <= 1.0
```

## Test Fixtures

### Shared Fixtures (conftest.py)
```python
# tests/conftest.py

import pytest
from gesture_processor import GestureProcessor
from facial_detector import FacialDetector
from config import Config, reset_config

@pytest.fixture(autouse=True)
def reset_global_config():
    """Reset global config before each test."""
    reset_config()
    yield
    reset_config()

@pytest.fixture
def gesture_processor():
    """Create GestureProcessor instance."""
    return GestureProcessor()

@pytest.fixture
def facial_detector():
    """Create FacialDetector instance."""
    return FacialDetector()

@pytest.fixture
def test_config():
    """Create test configuration."""
    config = Config()
    config.camera.width = 640
    config.camera.height = 480
    return config

@pytest.fixture
def mock_gesture_data():
    """Create mock gesture data."""
    return {
        'gesture_type': 'thumbs_up',
        'confidence': 0.92,
        'details': {}
    }
```

### Using Fixtures
```python
def test_process_gesture_data(gesture_processor, mock_gesture_data):
    """Test with multiple fixtures."""
    result = gesture_processor.analyze_gesture(mock_gesture_data)
    assert result is not None
```

## Mocking

### Mock Configuration
```python
from unittest.mock import Mock, patch
from action_executor import ActionExecutor

class TestActionExecutor:
    def test_open_whatsapp_mocked(self):
        """Test whatsapp opening with mocked subprocess."""
        with patch('subprocess.run') as mock_run:
            executor = ActionExecutor()
            result = executor.open_whatsapp()
            
            # Verify subprocess was called
            mock_run.assert_called_once()
            assert result['status'] == 'success'
```

### Mock Objects
```python
from unittest.mock import Mock
from gesture_processor import GestureProcessor

def test_gesture_callback():
    """Test gesture callback system."""
    processor = GestureProcessor()
    callback_mock = Mock()
    
    processor.register_gesture_callback(callback_mock)
    # Trigger gesture
    processor.analyze_gesture({})
    
    # Verify callback was called
    callback_mock.assert_called()
```

### Patching
```python
from unittest.mock import patch
from voice_commander import VoiceCommander

def test_voice_recognition():
    """Test voice command with mocked speech recognition."""
    with patch('speech_recognition.Recognizer') as mock_recognizer:
        mock_instance = mock_recognizer.return_value
        mock_instance.listen.return_value = "test audio"
        
        commander = VoiceCommander(command_callback=lambda x, y: None)
        # Test implementation
```

## Coverage

### Understanding Coverage
- **Statement Coverage**: How many lines were executed?
- **Branch Coverage**: How many if/else branches were tested?
- **Function Coverage**: How many functions were tested?

### Coverage Goals
- Minimum: 70%
- Target: 80%
- Ideal: 90%+

### Identify Uncovered Lines
```bash
# Show uncovered lines in terminal
pytest --cov=gesture_processor --cov-report=term-missing

# Example output:
# gesture_processor.py   187   10    95%   34, 67, 89-92, 156
# (lines 34, 67, 89-92, 156 not covered)
```

### Coverage Configuration (pyproject.toml)
```toml
[tool.pytest.ini_options]
addopts = "--cov=. --cov-report=term-missing --cov-report=html"
testpaths = ["tests"]
```

## CI/CD Integration

### GitHub Actions Workflow
```yaml
# .github/workflows/tests.yml

name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}
      
      - name: Install dependencies
        run: |
          pip install -e ".[dev]"
      
      - name: Run tests
        run: pytest --cov=. --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Best Practices

### 1. Test Isolation
```python
# Good: Each test is independent
def test_gesture_1(gesture_processor):
    result = gesture_processor.analyze_gesture({})
    assert result is not None

def test_gesture_2(gesture_processor):
    result = gesture_processor.analyze_gesture({})
    assert result is not None

# Bad: Tests depend on execution order
test_state = None

def test_first():
    global test_state
    test_state = "initialized"

def test_second():
    assert test_state == "initialized"  # Depends on test_first
```

### 2. Clear Test Names
```python
# Good: Clearly describes what is being tested
def test_thumbs_up_with_high_confidence(self):
    pass

# Bad: Unclear what is tested
def test_gesture(self):
    pass
```

### 3. Arrange-Act-Assert Pattern
```python
def test_analyze_gesture(self):
    """Test gesture analysis using AAA pattern."""
    # Arrange
    processor = GestureProcessor()
    gesture_data = {'gesture_type': 'thumbs_up'}
    
    # Act
    result = processor.analyze_gesture(gesture_data)
    
    # Assert
    assert result['gesture_type'] == 'thumbs_up'
```

### 4. One Assertion per Test (when possible)
```python
# Good: Isolated assertions
def test_gesture_type_is_thumbs_up(self):
    assert result['gesture_type'] == 'thumbs_up'

def test_gesture_confidence_is_high(self):
    assert result['confidence'] > 0.8

# Acceptable: Related assertions
def test_gesture_detection_complete(self):
    assert result['gesture_type'] == 'thumbs_up'
    assert result['confidence'] > 0.8
    assert 'details' in result
```

## Troubleshooting

### Test Failures

**Issue**: Tests pass locally but fail in CI
```bash
# Solution: Run tests in isolated environment
pytest --tb=short  # Show shorter traceback
pytest -vv         # Very verbose output
```

**Issue**: Flaky tests (fail intermittently)
```bash
# Solution: Run specific test multiple times
pytest --count=10 tests/unit/test_gesture_processor.py::test_detect_thumbs_up
```

**Issue**: Slow tests
```bash
# Solution: Identify slow tests
pytest --durations=10
```

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest Best Practices](https://docs.pytest.org/en/stable/goodpractices.html)
- [Testing is Documentation](https://docs.pytest.org/en/stable/example/parametrize.html)
