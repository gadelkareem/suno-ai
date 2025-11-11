# Suno AI Music Tools

[![Tests](https://github.com/gadelkareem/suno-ai/actions/workflows/tests.yml/badge.svg)](https://github.com/gadelkareem/suno-ai/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen.svg)](https://github.com/gadelkareem/suno-ai)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A comprehensive collection of tools for automating downloads and managing Suno AI generated music files. The flagship feature is a fully automated downloader that uses browser automation to handle authentication, filtering, and multi-format downloads.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [macOS](#macos-quick-setup)
  - [Linux](#linux)
  - [Windows](#windows)
- [Quick Start](#quick-start)
- [Automated Downloader](#automated-downloader)
  - [Usage Examples](#usage-examples)
  - [Configuration File](#configuration-file)
  - [Command-Line Options](#command-line-options)
  - [Filtering Options](#filtering-options)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Security Best Practices](#security-best-practices)
- [Other Tools](#other-tools)
- [Development](#development)
- [FAQ](#faq)
- [Contributing](#contributing)
- [License](#license)

## Features

### Automated Downloader (automated_downloader.py)

- **🤖 Fully Automated**: No manual clicking - logs in and downloads everything automatically
- **🎵 Multi-Format Support**: Download MP3, MP4 (video), and WAV formats
- **⏳ Smart Waiting**: Automatically waits for WAV and video generation to complete (up to 5 minutes configurable)
- **🔍 Advanced Filtering**: Filter by title, date range, completion status, video/audio availability
- **👁️ Visual UI**: Chrome browser with visible UI for monitoring progress (or headless mode)
- **📝 Detailed Logging**: Comprehensive logs to both console and file
- **🔐 Secure Config**: Store credentials in a config file (git-ignored for security)
- **📊 Progress Tracking**: Real-time progress updates and download statistics
- **🔄 Resume Support**: Skips already downloaded files automatically
- **🎯 Intelligent Selectors**: Multiple fallback strategies for robust login handling

### Additional Tools

- **Copy WAV Random**: Organize and transliterate WAV files with random prefixes
- **Duplicate Checker**: Find duplicate files using MD5 hash comparison
- **Batch Downloader**: Download from a list of URLs
- **Browser Script**: Extract download URLs from Suno AI web interface

## Prerequisites

Before installing, ensure you have:

### Required Software

1. **Python 3.8 or higher**
   - Check version: `python3 --version`
   - Download: https://www.python.org/downloads/

2. **Google Chrome Browser**
   - Download: https://www.google.com/chrome/
   - Required for browser automation (even in headless mode)

3. **pip (Python Package Manager)**
   - Usually included with Python
   - Check: `pip3 --version`

### System Requirements

- **Disk Space**: At least 1GB free space for downloads
- **Internet**: Stable internet connection for downloading files
- **RAM**: 2GB minimum (4GB recommended for large libraries)
- **OS**: macOS, Linux, or Windows

## Installation

### macOS Quick Setup

**Recommended for macOS users** - Use our automated setup script:

```bash
# 1. Clone the repository
git clone https://github.com/gadelkareem/suno-ai.git
cd suno-ai

# 2. Run the macOS setup script
chmod +x run_mac.sh
./run_mac.sh
```

The script will:
- Check for Python 3 and Chrome
- Create a virtual environment
- Install all dependencies
- Set up your config file
- Run the downloader

📖 For detailed macOS instructions, see [README_MAC.md](README_MAC.md)

### Linux

#### Ubuntu/Debian

```bash
# 1. Install Python 3 and pip (if not already installed)
sudo apt update
sudo apt install python3 python3-pip python3-venv

# 2. Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-get install -f  # Fix dependencies

# 3. Clone the repository
git clone https://github.com/gadelkareem/suno-ai.git
cd suno-ai

# 4. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Set up configuration
cp config.example.json config.json
nano config.json  # Edit with your credentials
```

#### Fedora/RHEL/CentOS

```bash
# 1. Install Python 3
sudo dnf install python3 python3-pip

# 2. Install Google Chrome
sudo dnf install https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm

# 3. Follow steps 3-6 from Ubuntu instructions above
```

### Windows

#### Option 1: Using PowerShell (Recommended)

```powershell
# 1. Install Python from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH" during installation

# 2. Install Google Chrome from https://www.google.com/chrome/

# 3. Clone repository (or download ZIP from GitHub)
git clone https://github.com/gadelkareem/suno-ai.git
cd suno-ai

# 4. Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 5. Install dependencies
pip install -r requirements.txt

# 6. Set up configuration
copy config.example.json config.json
notepad config.json  # Edit with your credentials
```

#### Option 2: Using Command Prompt

```cmd
# Follow same steps as PowerShell, but use:
venv\Scripts\activate.bat  # Instead of Activate.ps1
```

### Verify Installation

After installation, verify everything is working:

```bash
# Check Python version
python3 --version  # Should be 3.8 or higher

# Check Chrome installation
google-chrome --version  # Linux/Mac
# or
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version  # Windows

# Test the downloader (will show help)
python3 automated_downloader.py --help
```

## Quick Start

### 1. Basic Usage (Command Line)

```bash
python3 automated_downloader.py -u your-email@example.com -p your-password
```

This will:
- Log in to Suno AI
- Download all songs in all formats (MP3, MP4, WAV)
- Save to `./downloads` directory
- Show browser window during operation

### 2. Using Config File (Recommended)

```bash
# Create config from template
cp config.example.json config.json

# Edit config with your editor
nano config.json  # or vim, code, notepad, etc.

# Run with config
python3 automated_downloader.py -c config.json
```

### 3. macOS One-Liner

```bash
./run_mac.sh
```

## Automated Downloader

### Usage Examples

#### Basic Downloads

```bash
# Download everything (all songs, all formats)
python3 automated_downloader.py -u user@example.com -p password

# Download only MP3 files
python3 automated_downloader.py -u user@example.com -p password -f mp3

# Download MP3 and MP4 only (skip WAV)
python3 automated_downloader.py -u user@example.com -p password -f mp3 mp4

# Download to specific directory
python3 automated_downloader.py -u user@example.com -p password -o /path/to/music
```

#### Filtering Examples

```bash
# Download songs with "love" in the title
python3 automated_downloader.py -u user@example.com -p password --filter-title love

# Download only completed songs
python3 automated_downloader.py -u user@example.com -p password --filter-status complete

# Download songs created after January 1, 2025
python3 automated_downloader.py -u user@example.com -p password --min-date 2025-01-01

# Download songs from January 2025 only
python3 automated_downloader.py -u user@example.com -p password \
  --min-date 2025-01-01 --max-date 2025-01-31

# Download only songs with video
python3 automated_downloader.py -u user@example.com -p password --has-video

# Download only songs without video (audio-only)
python3 automated_downloader.py -u user@example.com -p password --no-video
```

#### Advanced Options

```bash
# Run in headless mode (no browser window)
python3 automated_downloader.py -u user@example.com -p password --headless

# Don't wait for generation (skip incomplete songs)
python3 automated_downloader.py -u user@example.com -p password --no-wait

# Wait longer for generation (10 minutes instead of 5)
python3 automated_downloader.py -c config.json  # Set max_wait_time: 600 in config

# Combine multiple options
python3 automated_downloader.py \
  -u user@example.com \
  -p password \
  -o ~/Music/Suno \
  -f mp3 wav \
  --filter-title "beat" \
  --has-video \
  --headless
```

#### Using Config File

```bash
# Basic usage with config
python3 automated_downloader.py -c config.json

# Config file with CLI overrides
python3 automated_downloader.py -c config.json -o /different/path

# Headless mode via config
python3 automated_downloader.py -c config.json  # Set "headless": true in config
```

### Configuration File

Create `config.json` from the template:

```json
{
  "credentials": {
    "username": "your-email@example.com",
    "password": "your-password"
  },
  "download": {
    "output_dir": "downloads",
    "formats": ["mp3", "mp4", "wav"],
    "wait_for_generation": true,
    "max_wait_time": 300
  },
  "browser": {
    "headless": false
  },
  "filters": {
    "title": "",
    "status": "",
    "has_video": null,
    "has_audio": null,
    "min_date": "",
    "max_date": ""
  }
}
```

#### Configuration Options Explained

**credentials:**
- `username`: Your Suno AI email address
- `password`: Your Suno AI password

**download:**
- `output_dir`: Where to save downloaded files (default: "downloads")
- `formats`: Array of formats to download - ["mp3", "mp4", "wav"]
- `wait_for_generation`: Wait for WAV/video to finish generating (true/false)
- `max_wait_time`: Maximum seconds to wait for generation (default: 300 = 5 minutes)

**browser:**
- `headless`: Run Chrome without visible window (true/false)

**filters:**
- `title`: Filter songs containing this text (case-insensitive, empty = all)
- `status`: Filter by status: "complete", "streaming", etc. (empty = all)
- `has_video`: true = only with video, false = only without video, null = all
- `has_audio`: true = only with audio, false = only without audio, null = all
- `min_date`: Minimum creation date in YYYY-MM-DD format (empty = no minimum)
- `max_date`: Maximum creation date in YYYY-MM-DD format (empty = no maximum)

### Command-Line Options

Complete list of command-line arguments:

```
Required (choose one):
  -c, --config PATH         Path to config.json file
  -u, --username EMAIL      Suno AI username/email
  -p, --password PASSWORD   Suno AI password

Optional:
  -o, --output DIR          Output directory (default: downloads)
  -f, --formats FORMAT ...  Formats to download: mp3, mp4, wav (default: all)
  --headless               Run browser in headless mode (no window)
  --no-wait                Don't wait for song generation to complete
  --help                   Show help message and exit

Filtering Options:
  --filter-title TEXT      Filter by title (contains, case-insensitive)
  --filter-status STATUS   Filter by status (complete, streaming, etc.)
  --has-video             Only download songs with video
  --no-video              Only download songs without video
  --has-audio             Only download songs with audio
  --no-audio              Only download songs without audio
  --min-date YYYY-MM-DD   Minimum creation date
  --max-date YYYY-MM-DD   Maximum creation date
```

### Filtering Options

#### Filter by Title

```bash
# Songs containing "love" (case-insensitive)
--filter-title love

# Songs containing "beat"
--filter-title "beat"

# Songs containing multiple words
--filter-title "my song"
```

#### Filter by Date

```bash
# Songs created in 2025
--min-date 2025-01-01

# Songs created before February 2025
--max-date 2025-02-01

# Songs created in January 2025
--min-date 2025-01-01 --max-date 2025-01-31

# Recent songs (last week)
--min-date 2025-11-04
```

#### Filter by Media Type

```bash
# Only songs with video
--has-video

# Only songs without video (audio-only)
--no-video

# Only songs with audio
--has-audio

# Songs without audio (rare, but possible)
--no-audio
```

#### Filter by Status

```bash
# Only completed songs
--filter-status complete

# Only streaming songs
--filter-status streaming
```

#### Combine Filters

```bash
# Completed songs with "love" in title, created in January 2025, with video
python3 automated_downloader.py \
  -u user@example.com -p password \
  --filter-title "love" \
  --filter-status complete \
  --min-date 2025-01-01 \
  --max-date 2025-01-31 \
  --has-video
```

## How It Works

### Architecture

The automated downloader uses Selenium WebDriver to automate Chrome browser:

```
┌─────────────────────────────────────────────────────────────┐
│                    User Provides Credentials                │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              1. Launch Chrome with Selenium                 │
│                 (Visible or Headless Mode)                  │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│            2. Navigate to Suno AI Login Page                │
│         (Multiple selector strategies for reliability)      │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              3. Enter Credentials and Login                 │
│          (Automatic form filling and submission)            │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              4. Navigate to Songs Library                   │
│               (Wait for page to fully load)                 │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│         5. Infinite Scroll to Load All Songs                │
│        (JavaScript execution to trigger lazy loading)       │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│        6. Extract Song Data from React Components           │
│      (JavaScript to read from __reactProps$ properties)     │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              7. Apply User-Specified Filters                │
│     (Title, date, status, video/audio availability)         │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│           8. Wait for Generation (if enabled)               │
│    (Poll every 10s for WAV/video completion, max 5 min)     │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│        9. Download Files in Selected Formats                │
│      (Streaming download with progress tracking)            │
└─────────────────────────┬───────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              10. Save to Output Directory                   │
│          (Organized by song title, skip existing)           │
└─────────────────────────────────────────────────────────────┘
```

### Key Technologies

- **Selenium WebDriver**: Browser automation framework
- **Chrome WebDriver Manager**: Automatic ChromeDriver installation and management
- **Python Requests**: HTTP library for downloading files
- **JavaScript Execution**: DOM manipulation and data extraction
- **React Props Extraction**: Reading data from React component internals

### Login Process Details

The login automation uses multiple strategies for robustness:

1. **Email Input**: Tries 6 different CSS selectors
2. **Password Input**: Tries 3 different CSS selectors
3. **Login Button**: Tries CSS selectors first, then XPath selectors
4. **URL Verification**: Checks if login was successful by detecting URL change

This multi-strategy approach ensures reliability even if Suno AI updates their UI.

### Infinite Scroll Implementation

```javascript
// JavaScript executed in browser to load all songs
let lastHeight = document.body.scrollHeight;
window.scrollTo(0, document.body.scrollHeight);
// Wait and compare heights to detect when loading completes
```

The downloader scrolls up to 20 times, waiting 2 seconds between each scroll for content to load.

### Song Data Extraction

```javascript
// Extract data from React components
const songs = [];
document.querySelectorAll('[class*="SongCard"]').forEach(card => {
  const reactProps = Object.keys(card).find(key => key.startsWith('__reactProps$'));
  if (card[reactProps]?.song) {
    songs.push(card[reactProps].song);
  }
});
```

This technique directly reads from React's internal properties, making it more reliable than parsing HTML.

## Troubleshooting

### Common Issues and Solutions

#### "Chrome WebDriver not found" or WebDriver errors

**Solution 1**: The script automatically downloads ChromeDriver, but if it fails:
```bash
# Linux/Mac
pip install --upgrade webdriver-manager

# If that doesn't work, manually install ChromeDriver:
# Download from https://chromedriver.chromium.org/downloads
# Place in /usr/local/bin/ (Mac/Linux) or C:\Windows\ (Windows)
```

**Solution 2**: Check Chrome version matches ChromeDriver:
```bash
google-chrome --version
# Download matching ChromeDriver version
```

#### "Login failed" or stuck on login page

**Possible causes**:
1. Incorrect username/password
2. Two-factor authentication enabled
3. Suno AI changed their login page structure

**Solutions**:
```bash
# 1. Verify credentials
python3 automated_downloader.py -u your@email.com -p password --no-headless

# 2. Check for 2FA - currently not supported
# You may need to disable 2FA temporarily

# 3. Check the logs
tail -f suno_downloader.log

# 4. Try without headless mode to see what's happening
python3 automated_downloader.py -u user@email.com -p password
```

#### "No songs found" or empty library

**Possible causes**:
1. Filters too restrictive
2. Songs not loading (scroll issue)
3. No songs in account

**Solutions**:
```bash
# Remove all filters
python3 automated_downloader.py -u user@email.com -p password

# Check logs for scroll information
grep "Scrolling" suno_downloader.log

# Run with visible browser to watch what happens
python3 automated_downloader.py -u user@email.com -p password
```

#### Downloads failing or incomplete

**Possible causes**:
1. Network issues
2. Insufficient disk space
3. Permission issues

**Solutions**:
```bash
# Check disk space
df -h  # Linux/Mac
# or
dir  # Windows

# Check permissions
ls -la downloads/  # Linux/Mac

# Try different output directory
python3 automated_downloader.py -u user@email.com -p password -o ~/Desktop/music

# Check network connectivity
ping google.com
```

#### "ModuleNotFoundError: No module named 'selenium'"

**Solution**:
```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Reinstall dependencies
pip install -r requirements.txt

# Or install manually
pip install selenium requests webdriver-manager
```

#### Chrome closes immediately or crashes

**Possible causes**:
1. ChromeDriver version mismatch
2. Chrome not properly installed
3. Conflicting Chrome instances

**Solutions**:
```bash
# Close all Chrome windows first
pkill chrome  # Linux/Mac
# or manually close all Chrome windows on Windows

# Update webdriver-manager
pip install --upgrade webdriver-manager

# Try headless mode
python3 automated_downloader.py -u user@email.com -p password --headless
```

#### Slow download speeds

**Solutions**:
```bash
# Download only specific formats
python3 automated_downloader.py -u user@email.com -p password -f mp3

# Don't wait for generation
python3 automated_downloader.py -u user@email.com -p password --no-wait

# Check network speed
speedtest-cli  # If installed
```

#### macOS: "Permission denied" when running run_mac.sh

**Solution**:
```bash
# Make script executable
chmod +x run_mac.sh

# Then run
./run_mac.sh
```

#### macOS: "Chrome quit unexpectedly"

**Solution**:
```bash
# Update Chrome to latest version
# Check: Chrome -> About Google Chrome

# Or try headless mode
./run_mac.sh --headless
```

#### Windows: "Scripts execution is disabled"

**Solution** (Run PowerShell as Administrator):
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Debugging

#### Enable verbose logging

Check the log file for detailed information:
```bash
tail -f suno_downloader.log  # Linux/Mac
Get-Content suno_downloader.log -Wait  # Windows PowerShell
```

The log includes:
- Login attempts and results
- Number of songs found
- Filter applications
- Download progress
- Errors and stack traces

#### Run with visible browser

Remove `--headless` flag to watch what the automation is doing:
```bash
python3 automated_downloader.py -u user@email.com -p password
```

You can watch the browser:
- Navigate to login page
- Fill in credentials
- Load songs
- Scroll through library
- Extract data

#### Check song data extraction

To see what songs were found, look in the logs:
```bash
grep "Found.*songs" suno_downloader.log
grep "After filtering" suno_downloader.log
```

### Getting Help

If you're still experiencing issues:

1. **Check the logs**: `suno_downloader.log` has detailed error messages
2. **Run in visible mode**: Remove `--headless` to see what's happening
3. **Check GitHub Issues**: https://github.com/gadelkareem/suno-ai/issues
4. **Create an issue**: Include your log file (remove sensitive info first)

## Security Best Practices

### Protecting Your Credentials

1. **Use Config File (Recommended)**:
   ```bash
   # config.json is in .gitignore - won't be committed to git
   cp config.example.json config.json
   nano config.json
   ```

2. **Avoid Command-Line Passwords**:
   ```bash
   # ❌ BAD - password visible in shell history
   python3 automated_downloader.py -u user@example.com -p mypassword

   # ✅ GOOD - use config file
   python3 automated_downloader.py -c config.json
   ```

3. **Set Proper Permissions**:
   ```bash
   # Make config readable only by you
   chmod 600 config.json  # Linux/Mac
   ```

4. **Don't Share Config**:
   - Never commit `config.json` to version control
   - Don't share screenshots containing credentials
   - Be careful when sharing logs (may contain usernames)

5. **Use Environment Variables** (Alternative):
   ```bash
   # Set in your shell
   export SUNO_USER="your@email.com"
   export SUNO_PASS="yourpassword"

   # Reference in script (requires code modification)
   ```

### Network Security

- The script uses HTTPS for all Suno AI communication
- Downloads are streamed directly from Suno's servers
- No credentials are sent to third parties
- All browser automation is local

### What Data Is Collected?

**Nothing is sent to external servers except Suno AI**:
- Credentials: Only sent to Suno AI login
- Song data: Extracted locally from browser
- Downloads: Directly from Suno AI servers
- Logs: Stored locally in `suno_downloader.log`

## Other Tools

### copy_wav_random.py

Copies WAV files to a destination directory with random number prefixes and transliterated filenames.

**Features**:
- Recursive scanning of source directory for WAV files
- Random number prefixing (10, 20, 30, etc.)
- Arabic to English filename transliteration
- Maintains original file metadata

**Usage**:
```bash
python3 copy_wav_random.py
```

The script will prompt you for:
- Source directory (where WAV files are)
- Destination directory (where to copy them)

### check_duplicates.py

Scans directories for duplicate files using MD5 hash comparison.

**Features**:
- Efficient handling of large files through chunked reading
- Shows file sizes for duplicates
- Recursive directory scanning
- Detailed reporting of duplicate files

**Usage**:
```bash
python3 check_duplicates.py
```

The script will prompt you for:
- Directory to scan

**Example output**:
```
Found duplicates:
  /path/to/song1.mp3 (3.5 MB)
  /path/to/song1_copy.mp3 (3.5 MB)
```

### suno-downloader.py

Downloads audio/video files from Suno.ai using a list of URLs.

**Features**:
- Handles both audio and video downloads
- Automatic file naming with conflict resolution
- Progress reporting
- Error handling for failed downloads

**Usage**:
```bash
# 1. Extract URLs using suno-download-all-songs.js
# 2. Save output to a file (e.g., urls.txt)
# 3. Run downloader
python3 suno-downloader.py urls.txt
```

### suno-download-all-songs.js

A browser-side JavaScript script to extract download URLs from Suno.ai's web interface.

**Features**:
- Extracts both audio and video URLs
- Formats output for use with suno-downloader.py
- Copies results to clipboard automatically

**Usage**:
1. Open Suno AI in your browser
2. Navigate to your songs library
3. Open browser developer console (F12)
4. Paste and execute the script
5. URLs are copied to clipboard
6. Save to a file and use with suno-downloader.py

## Development

### Running Tests

The project has comprehensive test coverage (99%) with a **minimum threshold of 95%** enforced in CI/CD.

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run tests with coverage report
pytest --cov=automated_downloader --cov-report=html

# View HTML coverage report
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows

# Run specific test file
pytest tests/test_automated_downloader.py

# Run specific test
pytest tests/test_automated_downloader.py::TestLogin::test_successful_login

# Check coverage threshold explicitly
coverage report --fail-under=95
```

**Coverage Requirements**:
- Minimum coverage: 95%
- Current coverage: 99%
- Branch coverage: Required
- CI/CD enforces threshold on all platforms

### Test Structure

```
tests/
├── __init__.py
├── conftest.py                      # Shared fixtures
├── test_automated_downloader.py     # Main test suite (42 tests)
└── test_extended_coverage.py        # Edge cases (12 tests)
```

### Code Quality

```bash
# Lint code (PEP 8 compliance)
flake8 automated_downloader.py

# Format code (consistent style)
black automated_downloader.py

# Sort imports (consistent organization)
isort automated_downloader.py

# Run all quality checks
flake8 automated_downloader.py && \
black --check automated_downloader.py && \
isort --check automated_downloader.py
```

**Quality Standards**:
- PEP 8 compliance
- Maximum line length: 100 characters
- Type hints for function signatures
- Comprehensive docstrings
- Error handling for all external calls

### Continuous Integration

Tests run automatically on GitHub Actions for every push and pull request.

**Test Matrix**:
- Python versions: 3.8, 3.9, 3.10, 3.11, 3.12
- Operating systems: Ubuntu, Windows, macOS

**CI Steps**:
1. Checkout code
2. Set up Python
3. Install dependencies
4. Run linters (flake8, black, isort)
5. Run tests with coverage
6. Check coverage threshold (95%)
7. Generate coverage badge and report
8. Upload coverage artifacts

See `.github/workflows/tests.yml` for full CI configuration.

### Contributing Guidelines

We welcome contributions! Here's how to contribute:

1. **Fork the repository**
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/my-new-feature
   ```

3. **Make your changes**:
   - Write code following the style guide
   - Add tests for new functionality
   - Ensure tests pass and coverage stays above 95%

4. **Test your changes**:
   ```bash
   pytest
   flake8 automated_downloader.py
   black automated_downloader.py
   isort automated_downloader.py
   ```

5. **Commit your changes**:
   ```bash
   git commit -m "Add feature: description of feature"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/my-new-feature
   ```

7. **Create a Pull Request**

**Code Review Process**:
- All PRs must pass CI/CD checks
- Code coverage must remain above 95%
- At least one maintainer approval required
- All conversations must be resolved

### Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/suno-ai.git
cd suno-ai

# Add upstream remote
git remote add upstream https://github.com/gadelkareem/suno-ai.git

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies (including dev dependencies)
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks (optional)
pre-commit install
```

## FAQ

### General Questions

**Q: Do I need a Suno AI subscription?**
A: Yes, you need a Suno AI account. The downloader logs in using your credentials.

**Q: Will this work if I change my password?**
A: You'll need to update your `config.json` with the new password.

**Q: Can I run this on a schedule/cron?**
A: Yes! Use headless mode and run via cron:
```bash
# Daily at 2am
0 2 * * * cd /path/to/suno-ai && ./venv/bin/python automated_downloader.py -c config.json --headless
```

**Q: How long does it take to download all songs?**
A: Depends on your library size and internet speed. For 100 songs with all formats, expect 30-60 minutes.

**Q: Does it work with free accounts?**
A: Yes, as long as you can access the songs in your browser.

### Technical Questions

**Q: Why does it use Selenium instead of API calls?**
A: Suno AI doesn't provide a public API. Browser automation is the most reliable method.

**Q: Can I run multiple instances simultaneously?**
A: Not recommended - might cause rate limiting or account issues.

**Q: Does it support two-factor authentication (2FA)?**
A: Currently no. You may need to temporarily disable 2FA.

**Q: Will this break if Suno AI updates their website?**
A: Possibly. The script uses multiple fallback selectors for robustness, but major UI changes may require updates.

**Q: Can I pause and resume downloads?**
A: The script skips already downloaded files, so you can stop and restart safely.

**Q: Does it download private/unlisted songs?**
A: Yes, it downloads all songs visible in your account.

### Troubleshooting Questions

**Q: Why is the browser closing immediately?**
A: Usually a ChromeDriver version mismatch. Update with: `pip install --upgrade webdriver-manager`

**Q: Why is it slow?**
A: Large files (especially WAV and video) take time. Try downloading only MP3 first.

**Q: Can I speed it up?**
A: Use `--no-wait` to skip incomplete songs, or download only specific formats with `-f mp3`.

**Q: What if I get "element not found" errors?**
A: Suno AI may have updated their UI. Check for script updates or file an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Selenium WebDriver for browser automation
- The Suno AI platform for music generation
- Contributors and testers who helped improve this tool

## Disclaimer

This tool is for personal use only. Please respect Suno AI's terms of service and do not use this tool for any commercial purposes or in violation of their policies. Always ensure you have the right to download and use the content you're accessing.

---

**Made with ❤️ for the Suno AI community**

For issues, questions, or contributions, visit: https://github.com/gadelkareem/suno-ai
