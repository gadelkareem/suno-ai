# Suno AI Music Tools

[![Tests](https://github.com/gadelkareem/suno-ai/actions/workflows/tests.yml/badge.svg)](https://github.com/gadelkareem/suno-ai/actions/workflows/tests.yml)
[![Coverage](https://img.shields.io/badge/coverage-84%25-green.svg)](https://github.com/gadelkareem/suno-ai)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A collection of tools for working with Suno AI generated music files.

## Features

- **Fully Automated Downloads**: Browser automation to login and download songs automatically
- **Multi-Format Support**: Download MP3, MP4, and WAV formats
- **Smart Filtering**: Filter songs by title, date, status, and more
- **Generation Waiting**: Automatically wait for WAV and video generation to complete
- **Visual UI**: Chrome browser controller with visible UI for monitoring
- Copy and organize WAV files with random numbering
- Transliterate Arabic filenames to English
- Support for recursive directory scanning
- Check for duplicate files
- Batch process audio files

## Scripts

### automated_downloader.py (NEW!)

**Fully automated downloader with browser automation** - The complete solution for downloading all your Suno AI songs without manual intervention. Features include:

- **Automated Login**: Logs in to Suno AI with your credentials
- **Browser Automation**: Uses Selenium with Chrome WebDriver for visual monitoring
- **Multi-Format Downloads**: Supports MP3, MP4, and WAV formats
- **Generation Waiting**: Waits for WAV and video files to finish generating
- **Advanced Filtering**: Filter by title, date, status, video/audio availability
- **Config File Support**: Store credentials and settings in a secure config file
- **Progress Logging**: Detailed logging to both file and console
- **Headless Mode**: Optional headless browser mode for running in background

#### Quick Start

1. **Install dependencies** (including Chrome WebDriver):
   ```bash
   pip install -r requirements.txt
   ```

2. **Create a config file** (recommended for security):
   ```bash
   cp config.example.json config.json
   # Edit config.json with your credentials
   ```

3. **Run the downloader**:
   ```bash
   # Using config file (recommended)
   python3 automated_downloader.py -c config.json

   # Or with command-line arguments
   python3 automated_downloader.py -u your-email@example.com -p your-password
   ```

#### Usage Examples

```bash
# Download all songs using config file
python3 automated_downloader.py -c config.json

# Download all songs in all formats (MP3, MP4, WAV)
python3 automated_downloader.py -u user@example.com -p password

# Download only MP3 and MP4 (skip WAV)
python3 automated_downloader.py -u user@example.com -p password -f mp3 mp4

# Download songs with title containing "love"
python3 automated_downloader.py -u user@example.com -p password --filter-title love

# Download to custom directory
python3 automated_downloader.py -u user@example.com -p password -o /path/to/downloads

# Run in headless mode (no visible browser)
python3 automated_downloader.py -u user@example.com -p password --headless

# Don't wait for generation (skip incomplete songs)
python3 automated_downloader.py -u user@example.com -p password --no-wait

# Filter by date range
python3 automated_downloader.py -u user@example.com -p password --min-date 2025-01-01

# Only download songs with video
python3 automated_downloader.py -u user@example.com -p password --has-video
```

#### Configuration File

Create a `config.json` file based on `config.example.json`:

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
    "status": "complete",
    "has_video": null,
    "has_audio": true,
    "min_date": "",
    "max_date": ""
  }
}
```

**Note**: `config.json` is ignored by git to protect your credentials.

#### Command-Line Options

- `-c, --config`: Path to config JSON file
- `-u, --username`: Suno AI username/email
- `-p, --password`: Suno AI password
- `-o, --output`: Output directory (default: downloads)
- `-f, --formats`: Formats to download: mp3, mp4, wav (default: all)
- `--headless`: Run browser in headless mode
- `--no-wait`: Don't wait for song generation
- `--filter-title`: Filter by title (contains)
- `--filter-status`: Filter by status (e.g., complete)
- `--has-video`: Only download songs with video
- `--has-audio`: Only download songs with audio
- `--min-date`: Minimum creation date (YYYY-MM-DD)
- `--max-date`: Maximum creation date (YYYY-MM-DD)

#### Logging

The downloader creates a log file `suno_downloader.log` with detailed information about the download process. Check this file if you encounter any issues.

### copy_wav_random.py

Copies WAV files to a destination directory with random number prefixes and transliterated filenames. Features include:
- Recursive scanning of source directory for WAV files
- Random number prefixing (10, 20, 30, etc.)
- Arabic to English filename transliteration
- Maintains original file metadata

Usage:
```bash
python3 copy_wav_random.py
```

### check_duplicates.py

Scans directories for duplicate files using MD5 hash comparison. Features include:
- Efficient handling of large files through chunked reading
- Shows file sizes for duplicates
- Recursive directory scanning
- Detailed reporting of duplicate files

Usage:
```bash
python3 check_duplicates.py
```

### suno-downloader.py

Downloads audio/video files from Suno.ai using a list of URLs. Features include:
- Handles both audio and video downloads
- Automatic file naming with conflict resolution
- Progress reporting
- Error handling for failed downloads

Usage:
```bash
python3 suno-downloader.py <path-to-js-output-file>
```

### suno-download-all-songs.js

A browser-side JavaScript script to extract download URLs from Suno.ai's web interface. Features include:
- Extracts both audio and video URLs
- Formats output for use with suno-downloader.py
- Copies results to clipboard automatically

Usage:
1. Open browser developer console on Suno.ai
2. Paste and execute the script
3. Use the output with suno-downloader.py

## Requirements

- Python 3.6+
- Required Python packages:
  - requests (for downloading files)
  - pathlib (for file operations)

## Installation

1. Clone the repository:
```bash
git clone git@github.com:gadelkareem/suno-ai.git
cd suno-ai
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the desired script:
```bash
python3 <script-name>.py
```

## Development

### Running Tests

The project has comprehensive test coverage (84%+). To run tests:

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage report
pytest --cov=automated_downloader --cov-report=html

# View coverage report
open htmlcov/index.html
```

### Code Quality

```bash
# Lint code
flake8 automated_downloader.py

# Format code
black automated_downloader.py

# Sort imports
isort automated_downloader.py
```

### Continuous Integration

Tests run automatically on GitHub Actions for:
- Python versions: 3.8, 3.9, 3.10, 3.11, 3.12
- Operating systems: Ubuntu, Windows, macOS

See `.github/workflows/tests.yml` for CI configuration.

## Notes

- Ensure you have sufficient disk space when working with audio/video files
- Some scripts may require configuration of source/destination paths
- Always verify downloaded files for integrity
