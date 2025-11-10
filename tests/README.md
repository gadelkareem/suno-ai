# Tests

Comprehensive test suite for the Suno AI Automated Downloader.

## Test Coverage

The test suite provides 100% code coverage for `automated_downloader.py`, including:

- **Initialization Tests**: Verify proper initialization with default and custom parameters
- **WebDriver Setup**: Test Chrome WebDriver configuration
- **Login Tests**: Test successful and failed login scenarios
- **Navigation Tests**: Test navigation to songs library
- **Scrolling Tests**: Test infinite scroll to load all songs
- **Song Extraction**: Test extracting song data from the page
- **Filtering Tests**: Test all filter types (title, date, status, media type)
- **Generation Waiting**: Test waiting for song generation
- **Download Tests**: Test file downloading with various scenarios
- **Error Handling**: Test error conditions and edge cases
- **Integration Tests**: Test complete workflow

## Running Tests

### Install Test Dependencies

```bash
pip install -r requirements-dev.txt
```

### Run All Tests

```bash
pytest
```

### Run with Coverage Report

```bash
pytest --cov=automated_downloader --cov-report=html
```

Then open `htmlcov/index.html` in your browser to view the coverage report.

### Run Specific Test Classes

```bash
# Run only initialization tests
pytest tests/test_automated_downloader.py::TestSunoDownloaderInit

# Run only filter tests
pytest tests/test_automated_downloader.py::TestApplyFilters

# Run only download tests
pytest tests/test_automated_downloader.py::TestDownloadFile
```

### Run with Verbose Output

```bash
pytest -v
```

### Run Tests Matching a Pattern

```bash
# Run tests with 'filter' in the name
pytest -k filter

# Run tests with 'download' in the name
pytest -k download
```

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py              # Shared fixtures and configuration
├── test_automated_downloader.py  # Main test file
└── README.md                # This file
```

## Fixtures

The `conftest.py` file provides shared fixtures:

- `temp_download_dir`: Temporary directory for download tests
- `mock_song_data`: Sample song data for testing
- `mock_webdriver`: Mock Selenium WebDriver
- `mock_wait`: Mock WebDriverWait
- `sample_config`: Sample configuration dictionary

## Continuous Integration

Tests run automatically on GitHub Actions for:

- Multiple Python versions (3.8, 3.9, 3.10, 3.11, 3.12)
- Multiple operating systems (Ubuntu, Windows, macOS)
- Pull requests and pushes to main branches

See `.github/workflows/tests.yml` for CI configuration.

## Code Quality

In addition to tests, the CI pipeline runs:

- **flake8**: Python linting
- **black**: Code formatting checks
- **isort**: Import sorting checks

Run these locally:

```bash
# Lint
flake8 automated_downloader.py

# Format code
black automated_downloader.py

# Sort imports
isort automated_downloader.py
```
