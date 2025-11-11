# Suno AI Automated Downloader - macOS Guide

Quick start guide for running the automated downloader on macOS.

## Prerequisites

1. **macOS** (10.14 or later recommended)
2. **Python 3.8+**
3. **Google Chrome** (for browser automation)

## Quick Start (3 Steps)

### 1. Download the Repository

```bash
# Clone the repository
git clone https://github.com/gadelkareem/suno-ai.git
cd suno-ai

# Or if you downloaded the ZIP, extract it and navigate to the folder
cd suno-ai-main
```

### 2. Run the Setup Script

```bash
./run_mac.sh
```

The script will:
- ✓ Check Python and Chrome installation
- ✓ Create a virtual environment
- ✓ Install all dependencies
- ✓ Create config.json from template
- ✓ Run the downloader

### 3. Configure Your Credentials

When prompted, edit `config.json` with your Suno AI credentials:

```json
{
  "credentials": {
    "username": "your-email@example.com",
    "password": "your-password"
  },
  "download": {
    "output_dir": "downloads",
    "formats": ["mp3", "mp4", "wav"]
  }
}
```

Save the file and press Enter to start downloading!

## Installation Issues?

### Python Not Found

Install Python using Homebrew:
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python3
```

Or download from: https://www.python.org/downloads/

### Chrome Not Found

Download and install Google Chrome from: https://www.google.com/chrome/

### Permission Denied

Make the script executable:
```bash
chmod +x run_mac.sh
```

## Usage Examples

### Basic Usage (with config file)

```bash
./run_mac.sh
```

### Command-Line Mode

```bash
# With username and password
./run_mac.sh --cli -u your-email@example.com -p your-password

# Download only MP3 and MP4
./run_mac.sh --cli -u your-email@example.com -p your-password -f "mp3 mp4"

# Run in headless mode (no browser window)
./run_mac.sh --headless

# Filter by title
./run_mac.sh --cli -u your-email@example.com -p your-password --filter-title "love"

# Custom output directory
./run_mac.sh --cli -u your-email@example.com -p your-password -o ~/Music/Suno

# Don't wait for generation (skip incomplete songs)
./run_mac.sh --no-wait
```

### Advanced Filtering

Edit `config.json` for advanced filtering:

```json
{
  "filters": {
    "title": "love",
    "status": "complete",
    "has_video": true,
    "has_audio": true,
    "min_date": "2025-01-01",
    "max_date": "2025-12-31"
  }
}
```

## What Gets Downloaded?

By default, the script downloads:
- 🎵 **MP3** - Audio files
- 🎥 **MP4** - Video files
- 🎼 **WAV** - High-quality audio (if available)

Files are saved to the `downloads/` folder with sanitized names.

## Browser Automation

The script uses Chrome to:
1. Log in to Suno AI with your credentials
2. Navigate to your songs library
3. Scroll through all your songs
4. Extract download URLs
5. Download files directly

You can watch the browser work, or use `--headless` to run it in the background.

## Troubleshooting

### "Chrome Driver Not Found"

The script will automatically download the correct ChromeDriver for your system. If it fails:

```bash
# Reinstall with verbose output
pip install selenium --upgrade
```

### "Login Failed"

- Check your username/password in config.json
- Make sure 2FA is not enabled on your Suno account
- Try logging in manually first to verify credentials

### "Permission Denied on Downloads"

```bash
# Give write permissions
chmod 755 downloads/
```

### Downloads Are Slow

- Check your internet connection
- Reduce formats: only download what you need (e.g., just MP3)
- Use `--no-wait` if you don't need WAV/video files

### Browser Keeps Crashing

```bash
# Try headless mode
./run_mac.sh --headless
```

## Logs and Debugging

Check `suno_downloader.log` for detailed information:

```bash
# View last 50 lines of log
tail -50 suno_downloader.log

# Watch log in real-time
tail -f suno_downloader.log
```

## Updating

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies
./run_mac.sh
```

## Security Notes

⚠️ **Your credentials are stored in `config.json`**

- This file is git-ignored for security
- Don't share this file
- Use a strong password
- Consider using an app-specific password if available

## Uninstalling

```bash
# Remove virtual environment
rm -rf venv/

# Remove downloads
rm -rf downloads/

# Remove config (contains credentials)
rm config.json

# Remove logs
rm suno_downloader.log
```

## Support

- **Issues**: https://github.com/gadelkareem/suno-ai/issues
- **Documentation**: https://github.com/gadelkareem/suno-ai
- **Tests**: Run `pytest` to verify installation

## macOS-Specific Tips

### Opening Downloads Folder

The script will offer to open the downloads folder when complete.

Or manually:
```bash
open downloads/
```

### Running in Background

```bash
# Run with headless mode and redirect output
./run_mac.sh --headless > output.log 2>&1 &

# Check progress
tail -f output.log
```

### Scheduling Downloads

Use cron to schedule regular downloads:

```bash
# Edit crontab
crontab -e

# Add line to download daily at 2 AM
0 2 * * * cd /path/to/suno-ai && ./run_mac.sh
```

### Adding to PATH

To run from anywhere:

```bash
# Add to ~/.zshrc or ~/.bashrc
echo 'alias suno-download="/path/to/suno-ai/run_mac.sh"' >> ~/.zshrc
source ~/.zshrc

# Now run from anywhere
suno-download
```

## Features

✓ **Fully Automated** - No manual clicking
✓ **Multi-Format** - MP3, MP4, WAV support
✓ **Smart Filtering** - By title, date, status
✓ **Wait for Generation** - Automatically waits for songs to finish
✓ **Visual Progress** - See browser automation in action
✓ **macOS Optimized** - Detects Chrome, opens files automatically
✓ **Virtual Environment** - Isolated Python dependencies
✓ **Logging** - Detailed logs for debugging

Enjoy your automated downloads! 🎵
