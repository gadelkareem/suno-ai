"""
Pytest configuration and shared fixtures
"""

import os
import sys
import pytest
import tempfile
from pathlib import Path
from unittest.mock import MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def temp_download_dir():
    """Create a temporary download directory"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_song_data():
    """Sample song data for testing"""
    return [
        {
            'id': 'song1',
            'title': 'Test Song 1',
            'audio_url': 'http://example.com/song1.mp3',
            'video_url': 'http://example.com/song1.mp4',
            'image_url': 'http://example.com/song1.jpg',
            'created_at': '2025-01-01T00:00:00Z',
            'duration': 180,
            'status': 'complete',
            'tags': []
        },
        {
            'id': 'song2',
            'title': 'Love Ballad',
            'audio_url': 'http://example.com/song2.mp3',
            'video_url': '',
            'image_url': 'http://example.com/song2.jpg',
            'created_at': '2025-01-15T00:00:00Z',
            'duration': 200,
            'status': 'complete',
            'tags': ['romantic']
        },
        {
            'id': 'song3',
            'title': 'Rock Anthem',
            'audio_url': '',
            'video_url': 'http://example.com/song3.mp4',
            'image_url': 'http://example.com/song3.jpg',
            'created_at': '2025-02-01T00:00:00Z',
            'duration': 240,
            'status': 'processing',
            'tags': ['rock']
        }
    ]


@pytest.fixture
def mock_webdriver():
    """Mock Selenium WebDriver"""
    driver = MagicMock()
    driver.current_url = "https://suno.com/songs"
    driver.execute_script.return_value = []
    return driver


@pytest.fixture
def mock_wait():
    """Mock WebDriverWait"""
    wait = MagicMock()
    return wait


@pytest.fixture
def sample_config():
    """Sample configuration dictionary"""
    return {
        "credentials": {
            "username": "test@example.com",
            "password": "testpass123"
        },
        "download": {
            "output_dir": "test_downloads",
            "formats": ["mp3", "mp4", "wav"],
            "wait_for_generation": True,
            "max_wait_time": 300
        },
        "browser": {
            "headless": False
        },
        "filters": {
            "title": "",
            "status": "complete",
            "has_video": None,
            "has_audio": True,
            "min_date": "",
            "max_date": ""
        }
    }
