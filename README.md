# Suno AI Music Tools

A collection of tools for working with Suno AI generated music files.

## Features

- Copy and organize WAV files with random numbering
- Transliterate Arabic filenames to English
- Support for recursive directory scanning
- Download songs from Suno.ai
- Check for duplicate files
- Batch process audio files

## Scripts

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

## Notes

- Ensure you have sufficient disk space when working with audio/video files
- Some scripts may require configuration of source/destination paths
- Always verify downloaded files for integrity
