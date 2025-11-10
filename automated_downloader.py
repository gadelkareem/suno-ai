#!/usr/bin/env python3
"""
Automated Suno AI Song Downloader
Fully automated script to login, browse, and download songs from Suno AI
"""

import os
import sys
import time
import json
import argparse
import logging
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('suno_downloader.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class SunoDownloader:
    """Automated downloader for Suno AI songs"""

    SUNO_URL = "https://suno.com"
    LOGIN_URL = "https://suno.com/login"
    LIBRARY_URL = "https://suno.com/songs"

    def __init__(self, username: str, password: str, download_dir: str = "downloads",
                 headless: bool = False, formats: List[str] = None):
        """
        Initialize the downloader

        Args:
            username: Suno AI username/email
            password: Suno AI password
            download_dir: Directory to save downloaded files
            headless: Run browser in headless mode
            formats: List of formats to download (mp3, mp4, wav)
        """
        self.username = username
        self.password = password
        self.download_dir = Path(download_dir)
        self.download_dir.mkdir(exist_ok=True)
        self.formats = formats or ['mp3', 'mp4', 'wav']
        self.driver = None
        self.headless = headless

        logger.info(f"Initialized downloader - Download dir: {self.download_dir}, Formats: {self.formats}")

    def setup_driver(self):
        """Setup Chrome WebDriver with appropriate options"""
        logger.info("Setting up Chrome WebDriver...")

        chrome_options = Options()

        # Basic options
        if self.headless:
            chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--start-maximized')

        # Disable automation flags
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Set user agent
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # Set download preferences
        prefs = {
            "download.default_directory": str(self.download_dir.absolute()),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        }
        chrome_options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

        logger.info("Chrome WebDriver initialized successfully")

    def login(self):
        """Login to Suno AI"""
        logger.info("Attempting to login to Suno AI...")

        try:
            self.driver.get(self.LOGIN_URL)
            time.sleep(3)

            # Wait for login form to load
            logger.info("Waiting for login form...")

            # Try to find email input field (adjust selectors as needed)
            email_selectors = [
                "input[type='email']",
                "input[name='email']",
                "input[placeholder*='email' i]",
                "input[placeholder*='Email' i]",
                "#email",
                "#username"
            ]

            email_input = None
            for selector in email_selectors:
                try:
                    email_input = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )
                    logger.info(f"Found email input with selector: {selector}")
                    break
                except TimeoutException:
                    continue

            if not email_input:
                logger.error("Could not find email input field")
                raise Exception("Email input field not found")

            # Enter email
            email_input.clear()
            email_input.send_keys(self.username)
            logger.info("Entered username/email")

            # Find password field
            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "#password"
            ]

            password_input = None
            for selector in password_selectors:
                try:
                    password_input = self.driver.find_element(By.CSS_SELECTOR, selector)
                    logger.info(f"Found password input with selector: {selector}")
                    break
                except NoSuchElementException:
                    continue

            if not password_input:
                logger.error("Could not find password input field")
                raise Exception("Password input field not found")

            # Enter password
            password_input.clear()
            password_input.send_keys(self.password)
            logger.info("Entered password")

            # Find and click login button
            login_button_selectors = [
                "button[type='submit']",
                "button:contains('Log in')",
                "button:contains('Sign in')",
                "input[type='submit']"
            ]

            login_button = None
            for selector in login_button_selectors:
                try:
                    login_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue

            if not login_button:
                # Try XPath as fallback
                try:
                    login_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Log') or contains(text(), 'Sign')]")
                except NoSuchElementException:
                    logger.error("Could not find login button")
                    raise Exception("Login button not found")

            login_button.click()
            logger.info("Clicked login button")

            # Wait for navigation after login
            time.sleep(5)

            # Check if login was successful
            if "login" not in self.driver.current_url.lower():
                logger.info("Login successful!")
                return True
            else:
                logger.warning("Still on login page, login may have failed")
                return False

        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            raise

    def navigate_to_library(self):
        """Navigate to the songs library"""
        logger.info("Navigating to songs library...")
        self.driver.get(self.LIBRARY_URL)
        time.sleep(3)

        # Wait for the songs grid to load
        try:
            self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[role='grid']"))
            )
            logger.info("Songs library loaded successfully")
        except TimeoutException:
            logger.warning("Timeout waiting for songs grid, but continuing...")

    def scroll_to_load_all_songs(self):
        """Scroll down to load all songs (lazy loading)"""
        logger.info("Scrolling to load all songs...")

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_attempts = 20

        while scroll_attempts < max_attempts:
            # Scroll down
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # Calculate new scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                logger.info("Reached end of page")
                break

            last_height = new_height
            scroll_attempts += 1
            logger.info(f"Scrolled {scroll_attempts} times...")

        # Scroll back to top
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        logger.info("Finished loading all songs")

    def extract_songs_data(self, filter_criteria: Optional[Dict] = None) -> List[Dict]:
        """
        Extract songs data from the page using JavaScript

        Args:
            filter_criteria: Dictionary with filter options:
                - title: Filter by title (contains)
                - min_date: Filter by minimum creation date
                - max_date: Filter by maximum creation date
                - has_video: Filter for songs with video
                - has_audio: Filter for songs with audio

        Returns:
            List of song dictionaries with metadata and URLs
        """
        logger.info("Extracting songs data from page...")

        # JavaScript to extract song data from React props
        js_script = """
        try {
            const grid = document.querySelector('[role="grid"]');
            if (!grid) return [];

            const reactPropsKey = Object.keys(grid).find(key => key.startsWith('__reactProps'));
            if (!reactPropsKey) return [];

            const songs = grid[reactPropsKey].children[0].props.values[0][1].collection;

            return [...songs]
                .filter(x => x.value && x.value.clip && x.value.clip.clip)
                .map(x => {
                    const clip = x.value.clip.clip;
                    return {
                        id: clip.id || '',
                        title: clip.title ? clip.title.trim() : clip.id,
                        audio_url: clip.audio_url || '',
                        video_url: clip.video_url || '',
                        image_url: clip.image_url || '',
                        created_at: clip.created_at || '',
                        duration: clip.duration || 0,
                        status: clip.status || '',
                        tags: clip.tags || []
                    };
                });
        } catch (e) {
            console.error('Error extracting songs:', e);
            return [];
        }
        """

        songs = self.driver.execute_script(js_script)
        logger.info(f"Extracted {len(songs)} songs from page")

        # Apply filters
        if filter_criteria:
            songs = self._apply_filters(songs, filter_criteria)
            logger.info(f"After filtering: {len(songs)} songs remain")

        return songs

    def _apply_filters(self, songs: List[Dict], criteria: Dict) -> List[Dict]:
        """Apply filter criteria to songs list"""
        filtered = songs

        # Filter by title
        if criteria.get('title'):
            title_filter = criteria['title'].lower()
            filtered = [s for s in filtered if title_filter in s['title'].lower()]
            logger.info(f"Filtered by title '{criteria['title']}': {len(filtered)} songs")

        # Filter by date range
        if criteria.get('min_date'):
            min_date = datetime.fromisoformat(criteria['min_date'])
            filtered = [s for s in filtered if s.get('created_at') and
                       datetime.fromisoformat(s['created_at'].replace('Z', '+00:00')) >= min_date]
            logger.info(f"Filtered by min_date: {len(filtered)} songs")

        if criteria.get('max_date'):
            max_date = datetime.fromisoformat(criteria['max_date'])
            filtered = [s for s in filtered if s.get('created_at') and
                       datetime.fromisoformat(s['created_at'].replace('Z', '+00:00')) <= max_date]
            logger.info(f"Filtered by max_date: {len(filtered)} songs")

        # Filter by has_video
        if criteria.get('has_video') is not None:
            if criteria['has_video']:
                filtered = [s for s in filtered if s.get('video_url')]
            else:
                filtered = [s for s in filtered if not s.get('video_url')]
            logger.info(f"Filtered by has_video: {len(filtered)} songs")

        # Filter by has_audio
        if criteria.get('has_audio') is not None:
            if criteria['has_audio']:
                filtered = [s for s in filtered if s.get('audio_url')]
            else:
                filtered = [s for s in filtered if not s.get('audio_url')]
            logger.info(f"Filtered by has_audio: {len(filtered)} songs")

        # Filter by status
        if criteria.get('status'):
            status = criteria['status'].lower()
            filtered = [s for s in filtered if s.get('status', '').lower() == status]
            logger.info(f"Filtered by status '{status}': {len(filtered)} songs")

        return filtered

    def wait_for_generation(self, song: Dict, max_wait_time: int = 300) -> Dict:
        """
        Wait for a song to finish generating (for WAV and video)

        Args:
            song: Song dictionary
            max_wait_time: Maximum time to wait in seconds

        Returns:
            Updated song dictionary
        """
        song_id = song['id']
        logger.info(f"Checking generation status for song: {song['title']} (ID: {song_id})")

        # Check if generation is complete
        status = song.get('status', '').lower()
        if status == 'complete':
            logger.info(f"Song already complete: {song['title']}")
            return song

        start_time = time.time()
        check_interval = 10  # Check every 10 seconds

        while time.time() - start_time < max_wait_time:
            logger.info(f"Waiting for generation... ({int(time.time() - start_time)}s elapsed)")
            time.sleep(check_interval)

            # Refresh page to get updated data
            self.driver.refresh()
            time.sleep(3)

            # Re-extract songs data
            songs = self.extract_songs_data()

            # Find our song
            updated_song = next((s for s in songs if s['id'] == song_id), None)

            if updated_song:
                status = updated_song.get('status', '').lower()
                if status == 'complete':
                    logger.info(f"Generation complete for: {updated_song['title']}")
                    return updated_song
                else:
                    logger.info(f"Status: {status}")

        logger.warning(f"Generation timeout for song: {song['title']}")
        return song

    def download_file(self, url: str, filename: str, file_type: str) -> bool:
        """
        Download a file from URL

        Args:
            url: Download URL
            filename: Filename to save as
            file_type: Type of file (mp3, mp4, wav)

        Returns:
            True if successful, False otherwise
        """
        if not url:
            logger.warning(f"No URL provided for {filename}")
            return False

        filepath = self.download_dir / filename

        # Skip if already exists
        if filepath.exists():
            logger.info(f"File already exists, skipping: {filename}")
            return True

        try:
            logger.info(f"Downloading {file_type.upper()}: {filename}")

            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)

                        # Log progress for large files
                        if total_size > 0 and downloaded % (1024 * 1024) == 0:  # Every MB
                            progress = (downloaded / total_size) * 100
                            logger.info(f"Progress: {progress:.1f}%")

            logger.info(f"Successfully downloaded: {filename}")
            return True

        except Exception as e:
            logger.error(f"Failed to download {filename}: {str(e)}")
            # Clean up partial file
            if filepath.exists():
                filepath.unlink()
            return False

    def get_wav_url(self, song: Dict) -> Optional[str]:
        """
        Try to get WAV URL for a song (might need API call or special logic)
        For now, we'll try to construct it based on patterns
        """
        # This is a placeholder - the actual WAV URL might need to be fetched differently
        # Some sites provide WAV through a different endpoint
        audio_url = song.get('audio_url', '')

        if audio_url:
            # Try replacing extension (might not always work)
            wav_url = audio_url.replace('.mp3', '.wav')
            # Or check if there's a specific WAV endpoint
            return wav_url

        return None

    def download_song(self, song: Dict, wait_for_gen: bool = True) -> Dict[str, bool]:
        """
        Download all requested formats for a song

        Args:
            song: Song dictionary
            wait_for_gen: Wait for generation if not complete

        Returns:
            Dictionary with download status for each format
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Processing song: {song['title']}")
        logger.info(f"{'='*60}")

        results = {}

        # Wait for generation if needed
        if wait_for_gen and song.get('status', '').lower() != 'complete':
            song = self.wait_for_generation(song)

        # Sanitize filename
        safe_title = "".join(c for c in song['title'] if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_title = safe_title or song['id']

        # Download MP3
        if 'mp3' in self.formats:
            filename = f"{safe_title}.mp3"
            results['mp3'] = self.download_file(song.get('audio_url', ''), filename, 'mp3')

        # Download MP4
        if 'mp4' in self.formats:
            filename = f"{safe_title}.mp4"
            results['mp4'] = self.download_file(song.get('video_url', ''), filename, 'mp4')

        # Download WAV
        if 'wav' in self.formats:
            filename = f"{safe_title}.wav"
            wav_url = self.get_wav_url(song)
            results['wav'] = self.download_file(wav_url, filename, 'wav')

        return results

    def run(self, filter_criteria: Optional[Dict] = None, wait_for_generation: bool = True):
        """
        Main execution method

        Args:
            filter_criteria: Dictionary with filter options
            wait_for_generation: Wait for songs to finish generating
        """
        try:
            # Setup browser
            self.setup_driver()

            # Login
            if not self.login():
                logger.error("Login failed, aborting...")
                return

            # Navigate to library
            self.navigate_to_library()

            # Load all songs
            self.scroll_to_load_all_songs()

            # Extract songs
            songs = self.extract_songs_data(filter_criteria)

            if not songs:
                logger.warning("No songs found matching criteria")
                return

            logger.info(f"\n{'='*60}")
            logger.info(f"Found {len(songs)} songs to download")
            logger.info(f"{'='*60}\n")

            # Download each song
            success_count = 0
            fail_count = 0

            for i, song in enumerate(songs, 1):
                logger.info(f"\nProcessing song {i}/{len(songs)}")

                try:
                    results = self.download_song(song, wait_for_gen=wait_for_generation)

                    if any(results.values()):
                        success_count += 1
                    else:
                        fail_count += 1

                except Exception as e:
                    logger.error(f"Error processing song {song['title']}: {str(e)}")
                    fail_count += 1

            logger.info(f"\n{'='*60}")
            logger.info(f"Download complete!")
            logger.info(f"Success: {success_count}, Failed: {fail_count}")
            logger.info(f"{'='*60}\n")

        except Exception as e:
            logger.error(f"Fatal error: {str(e)}", exc_info=True)
            raise

        finally:
            if self.driver:
                logger.info("Closing browser...")
                self.driver.quit()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Automated Suno AI Song Downloader',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all songs using config file
  python automated_downloader.py -c config.json

  # Download all songs in all formats
  python automated_downloader.py -u user@example.com -p password

  # Download only MP3 and MP4
  python automated_downloader.py -u user@example.com -p password -f mp3 mp4

  # Download songs with title containing "love"
  python automated_downloader.py -u user@example.com -p password --filter-title love

  # Download with custom output directory
  python automated_downloader.py -u user@example.com -p password -o /path/to/downloads

  # Run in headless mode (no visible browser)
  python automated_downloader.py -u user@example.com -p password --headless

  # Don't wait for generation (skip incomplete songs)
  python automated_downloader.py -u user@example.com -p password --no-wait
        """
    )

    # Config file
    parser.add_argument('-c', '--config',
                       help='Path to config JSON file')

    # Required arguments (can be provided via config)
    parser.add_argument('-u', '--username',
                       help='Suno AI username/email')
    parser.add_argument('-p', '--password',
                       help='Suno AI password')

    # Optional arguments
    parser.add_argument('-o', '--output', default='downloads',
                       help='Output directory for downloads (default: downloads)')
    parser.add_argument('-f', '--formats', nargs='+',
                       choices=['mp3', 'mp4', 'wav'],
                       default=['mp3', 'mp4', 'wav'],
                       help='Formats to download (default: all)')
    parser.add_argument('--headless', action='store_true',
                       help='Run browser in headless mode (no UI)')
    parser.add_argument('--no-wait', action='store_true',
                       help='Don\'t wait for song generation to complete')

    # Filter arguments
    parser.add_argument('--filter-title',
                       help='Filter songs by title (contains)')
    parser.add_argument('--filter-status',
                       help='Filter by status (e.g., complete, processing)')
    parser.add_argument('--has-video', action='store_true',
                       help='Only download songs with video')
    parser.add_argument('--has-audio', action='store_true',
                       help='Only download songs with audio')
    parser.add_argument('--min-date',
                       help='Minimum creation date (ISO format: YYYY-MM-DD)')
    parser.add_argument('--max-date',
                       help='Maximum creation date (ISO format: YYYY-MM-DD)')

    args = parser.parse_args()

    # Load config file if provided
    config = {}
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
            logger.info(f"Loaded configuration from {args.config}")
        except Exception as e:
            logger.error(f"Failed to load config file: {str(e)}")
            sys.exit(1)

    # Get credentials (command line overrides config)
    username = args.username or config.get('credentials', {}).get('username')
    password = args.password or config.get('credentials', {}).get('password')

    if not username or not password:
        logger.error("Username and password are required (via -u/-p or config file)")
        parser.print_help()
        sys.exit(1)

    # Get download settings (command line overrides config)
    download_config = config.get('download', {})
    output_dir = args.output if args.output != 'downloads' else download_config.get('output_dir', 'downloads')
    formats = args.formats if args.formats != ['mp3', 'mp4', 'wav'] else download_config.get('formats', ['mp3', 'mp4', 'wav'])
    wait_for_gen = download_config.get('wait_for_generation', True) if not args.no_wait else False

    # Get browser settings
    browser_config = config.get('browser', {})
    headless = args.headless or browser_config.get('headless', False)

    # Build filter criteria (command line overrides config)
    config_filters = config.get('filters', {})
    filter_criteria = {}

    if args.filter_title or config_filters.get('title'):
        filter_criteria['title'] = args.filter_title or config_filters.get('title')
    if args.filter_status or config_filters.get('status'):
        filter_criteria['status'] = args.filter_status or config_filters.get('status')
    if args.has_video or config_filters.get('has_video'):
        filter_criteria['has_video'] = True
    if args.has_audio or config_filters.get('has_audio'):
        filter_criteria['has_audio'] = True
    if args.min_date or config_filters.get('min_date'):
        filter_criteria['min_date'] = args.min_date or config_filters.get('min_date')
    if args.max_date or config_filters.get('max_date'):
        filter_criteria['max_date'] = args.max_date or config_filters.get('max_date')

    # Create downloader and run
    downloader = SunoDownloader(
        username=username,
        password=password,
        download_dir=output_dir,
        headless=headless,
        formats=formats
    )

    downloader.run(
        filter_criteria=filter_criteria if filter_criteria else None,
        wait_for_generation=wait_for_gen
    )


if __name__ == '__main__':
    main()
