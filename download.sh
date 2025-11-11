#!/bin/bash
# Convenience wrapper for automated_downloader.py

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if config.json exists
if [ -f "$SCRIPT_DIR/config.json" ]; then
    echo "Using config.json for credentials and settings..."
    python3 "$SCRIPT_DIR/automated_downloader.py" -c "$SCRIPT_DIR/config.json" "$@"
else
    echo "No config.json found. You can create one from config.example.json"
    echo "Running with command-line arguments..."
    python3 "$SCRIPT_DIR/automated_downloader.py" "$@"
fi
