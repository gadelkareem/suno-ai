#!/bin/bash
# Suno AI Automated Downloader - macOS Setup and Run Script
# This script sets up and runs the automated downloader on macOS

set -e  # Exit on error

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Suno AI Automated Downloader - macOS Setup         ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

# Function to print colored output
print_info() {
    echo -e "${BLUE}ℹ ${NC}$1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if Python 3 is installed
print_info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed."
    echo ""
    echo "Please install Python 3:"
    echo "  1. Using Homebrew: brew install python3"
    echo "  2. Download from: https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
print_success "Found $PYTHON_VERSION"

# Check if Chrome is installed
print_info "Checking Google Chrome installation..."
if [ ! -d "/Applications/Google Chrome.app" ]; then
    print_warning "Google Chrome not found in /Applications/"
    echo ""
    echo "This script requires Google Chrome for browser automation."
    echo "Please download and install Chrome from: https://www.google.com/chrome/"
    echo ""
    read -p "Press Enter after installing Chrome, or Ctrl+C to exit..."
fi
print_success "Google Chrome is installed"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_info "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip --quiet

# Install dependencies
print_info "Installing dependencies..."
if pip install -r requirements.txt --quiet; then
    print_success "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi

# Check for config file
echo ""
if [ ! -f "config.json" ]; then
    print_warning "Configuration file not found"
    echo ""
    echo "Creating config.json from template..."

    if [ -f "config.example.json" ]; then
        cp config.example.json config.json
        print_success "Created config.json"
        echo ""
        print_info "Please edit config.json with your Suno AI credentials:"
        echo "  - Open config.json in a text editor"
        echo "  - Update 'username' with your Suno AI email"
        echo "  - Update 'password' with your Suno AI password"
        echo "  - Optionally adjust download settings and filters"
        echo ""

        # Open config file in default editor on macOS
        if command -v open &> /dev/null; then
            read -p "Open config.json now? (y/n) " -n 1 -r
            echo ""
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                open -a TextEdit config.json
                echo ""
                print_info "Waiting for you to save the config file..."
                read -p "Press Enter when you've saved your credentials..."
            fi
        fi
    else
        print_error "config.example.json not found"
        exit 1
    fi
else
    print_success "Configuration file found"
fi

echo ""
print_success "Setup complete!"
echo ""

# Parse command line arguments
RUN_MODE="config"
EXTRA_ARGS=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --cli)
            RUN_MODE="cli"
            shift
            ;;
        --username|-u)
            USERNAME="$2"
            shift 2
            ;;
        --password|-p)
            PASSWORD="$2"
            shift 2
            ;;
        --formats|-f)
            FORMATS="$2"
            shift 2
            ;;
        --output|-o)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --filter-title)
            FILTER_TITLE="$2"
            shift 2
            ;;
        --headless)
            EXTRA_ARGS="$EXTRA_ARGS --headless"
            shift
            ;;
        --no-wait)
            EXTRA_ARGS="$EXTRA_ARGS --no-wait"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Run with config file (default):"
            echo "  $0"
            echo ""
            echo "Run with command-line arguments:"
            echo "  $0 --cli -u USERNAME -p PASSWORD [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -u, --username USER     Suno AI username/email"
            echo "  -p, --password PASS     Suno AI password"
            echo "  -f, --formats FORMATS   Formats to download (e.g., 'mp3 mp4 wav')"
            echo "  -o, --output DIR        Output directory"
            echo "  --filter-title TEXT     Filter by title"
            echo "  --headless              Run in headless mode (no browser window)"
            echo "  --no-wait               Don't wait for song generation"
            echo "  --help                  Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                                    # Use config.json"
            echo "  $0 --cli -u user@example.com -p pass  # Use CLI args"
            echo "  $0 --headless                         # Run without browser window"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Run the downloader
echo -e "${BLUE}╔═══════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Starting Automated Downloader                      ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════════╝${NC}"
echo ""

if [ "$RUN_MODE" = "cli" ]; then
    if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ]; then
        print_error "Username and password required in CLI mode"
        echo "Use: $0 --cli -u USERNAME -p PASSWORD"
        exit 1
    fi

    CMD="python3 automated_downloader.py -u \"$USERNAME\" -p \"$PASSWORD\""

    [ ! -z "$FORMATS" ] && CMD="$CMD -f $FORMATS"
    [ ! -z "$OUTPUT_DIR" ] && CMD="$CMD -o \"$OUTPUT_DIR\""
    [ ! -z "$FILTER_TITLE" ] && CMD="$CMD --filter-title \"$FILTER_TITLE\""
    [ ! -z "$EXTRA_ARGS" ] && CMD="$CMD $EXTRA_ARGS"

    print_info "Running with CLI arguments..."
    eval $CMD
else
    print_info "Running with config.json..."
    python3 automated_downloader.py -c config.json $EXTRA_ARGS
fi

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    print_success "Download completed successfully!"
    echo ""
    echo "Your files are in the downloads directory"

    # Offer to open downloads folder
    read -p "Open downloads folder? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        if [ -d "downloads" ]; then
            open downloads
        else
            print_warning "Downloads directory not found"
        fi
    fi
else
    print_error "Download failed with exit code $EXIT_CODE"
    echo ""
    echo "Check suno_downloader.log for details"
fi

# Deactivate virtual environment
deactivate

exit $EXIT_CODE
