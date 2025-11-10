"""
Comprehensive tests for automated_downloader.py
Covers all classes, methods, and edge cases
"""

import os
import sys
import json
import tempfile
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch, call, mock_open
from datetime import datetime

# Add parent directory to path to import the module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from automated_downloader import SunoDownloader


class TestSunoDownloaderInit:
    """Test SunoDownloader initialization"""

    def test_init_with_defaults(self):
        """Test initialization with default parameters"""
        downloader = SunoDownloader("user@test.com", "password123")

        assert downloader.username == "user@test.com"
        assert downloader.password == "password123"
        assert downloader.download_dir == Path("downloads")
        assert downloader.formats == ['mp3', 'mp4', 'wav']
        assert downloader.headless is False
        assert downloader.driver is None

    def test_init_with_custom_params(self):
        """Test initialization with custom parameters"""
        downloader = SunoDownloader(
            "custom@test.com",
            "pass456",
            download_dir="custom_downloads",
            headless=True,
            formats=['mp3', 'mp4']
        )

        assert downloader.username == "custom@test.com"
        assert downloader.password == "pass456"
        assert downloader.download_dir == Path("custom_downloads")
        assert downloader.formats == ['mp3', 'mp4']
        assert downloader.headless is True

    def test_download_dir_created(self):
        """Test that download directory is created"""
        with tempfile.TemporaryDirectory() as tmpdir:
            test_dir = os.path.join(tmpdir, "test_downloads")
            downloader = SunoDownloader("user@test.com", "password", download_dir=test_dir)

            assert os.path.exists(test_dir)


class TestSetupDriver:
    """Test Chrome WebDriver setup"""

    @patch('automated_downloader.webdriver.Chrome')
    def test_setup_driver_headless(self, mock_chrome):
        """Test driver setup in headless mode"""
        downloader = SunoDownloader("user@test.com", "password", headless=True)
        downloader.setup_driver()

        mock_chrome.assert_called_once()
        assert downloader.driver is not None

    @patch('automated_downloader.webdriver.Chrome')
    def test_setup_driver_visible(self, mock_chrome):
        """Test driver setup in visible mode"""
        downloader = SunoDownloader("user@test.com", "password", headless=False)
        downloader.setup_driver()

        mock_chrome.assert_called_once()
        assert downloader.driver is not None


class TestLogin:
    """Test login functionality"""

    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    def test_login_success(self, mock_sleep, mock_chrome):
        """Test successful login"""
        # Setup mocks
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_driver.current_url = "https://suno.com/songs"

        # Mock email input
        mock_email_input = MagicMock()
        # Mock password input
        mock_password_input = MagicMock()
        # Mock login button
        mock_login_button = MagicMock()

        mock_driver.find_element.side_effect = [
            mock_password_input,
            mock_login_button
        ]

        # Mock wait until
        mock_wait = MagicMock()
        mock_wait.until.return_value = mock_email_input

        downloader = SunoDownloader("user@test.com", "password")
        downloader.setup_driver()
        downloader.wait = mock_wait

        result = downloader.login()

        assert result is True
        mock_email_input.clear.assert_called_once()
        mock_email_input.send_keys.assert_called_once_with("user@test.com")
        mock_password_input.clear.assert_called_once()
        mock_password_input.send_keys.assert_called_once_with("password")
        mock_login_button.click.assert_called_once()

    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    def test_login_still_on_login_page(self, mock_sleep, mock_chrome):
        """Test login when still on login page after attempt"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_driver.current_url = "https://suno.com/login"

        mock_email_input = MagicMock()
        mock_password_input = MagicMock()
        mock_login_button = MagicMock()

        mock_driver.find_element.side_effect = [
            mock_password_input,
            mock_login_button
        ]

        mock_wait = MagicMock()
        mock_wait.until.return_value = mock_email_input

        downloader = SunoDownloader("user@test.com", "password")
        downloader.setup_driver()
        downloader.wait = mock_wait

        result = downloader.login()

        assert result is False


class TestNavigateToLibrary:
    """Test navigation to songs library"""

    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    def test_navigate_to_library_success(self, mock_sleep, mock_chrome):
        """Test successful navigation to library"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        mock_wait = MagicMock()
        mock_grid = MagicMock()
        mock_wait.until.return_value = mock_grid

        downloader = SunoDownloader("user@test.com", "password")
        downloader.setup_driver()
        downloader.wait = mock_wait

        downloader.navigate_to_library()

        mock_driver.get.assert_called_with(downloader.LIBRARY_URL)


class TestScrollToLoadAllSongs:
    """Test scrolling to load all songs"""

    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    def test_scroll_until_end(self, mock_sleep, mock_chrome):
        """Test scrolling until reaching the end"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        # Simulate scroll heights: 1000, 2000, 2000 (no change = end)
        heights = [1000, 2000, 2000]
        height_index = [0]

        def get_height(script):
            if 'scrollHeight' in script:
                result = heights[height_index[0]]
                height_index[0] = min(height_index[0] + 1, len(heights) - 1)
                return result
            return None

        mock_driver.execute_script.side_effect = get_height

        downloader = SunoDownloader("user@test.com", "password")
        downloader.setup_driver()

        downloader.scroll_to_load_all_songs()

        # Should have called execute_script multiple times
        assert mock_driver.execute_script.call_count >= 3


class TestExtractSongsData:
    """Test song data extraction from page"""

    @patch('automated_downloader.webdriver.Chrome')
    def test_extract_songs_success(self, mock_chrome):
        """Test successful song extraction"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        # Mock JavaScript execution to return song data
        mock_songs = [
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
                'title': 'Test Song 2',
                'audio_url': 'http://example.com/song2.mp3',
                'video_url': '',
                'image_url': 'http://example.com/song2.jpg',
                'created_at': '2025-01-02T00:00:00Z',
                'duration': 200,
                'status': 'complete',
                'tags': ['pop']
            }
        ]

        mock_driver.execute_script.return_value = mock_songs

        downloader = SunoDownloader("user@test.com", "password")
        downloader.setup_driver()

        songs = downloader.extract_songs_data()

        assert len(songs) == 2
        assert songs[0]['title'] == 'Test Song 1'
        assert songs[1]['title'] == 'Test Song 2'

    @patch('automated_downloader.webdriver.Chrome')
    def test_extract_songs_empty(self, mock_chrome):
        """Test extraction when no songs found"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_driver.execute_script.return_value = []

        downloader = SunoDownloader("user@test.com", "password")
        downloader.setup_driver()

        songs = downloader.extract_songs_data()

        assert len(songs) == 0


class TestApplyFilters:
    """Test filter application"""

    def setup_method(self):
        """Setup test data"""
        self.downloader = SunoDownloader("user@test.com", "password")
        self.songs = [
            {
                'id': 'song1',
                'title': 'Love Song',
                'audio_url': 'http://example.com/song1.mp3',
                'video_url': 'http://example.com/song1.mp4',
                'created_at': '2025-01-01T00:00:00Z',
                'status': 'complete'
            },
            {
                'id': 'song2',
                'title': 'Rock Anthem',
                'audio_url': 'http://example.com/song2.mp3',
                'video_url': '',
                'created_at': '2025-01-15T00:00:00Z',
                'status': 'complete'
            },
            {
                'id': 'song3',
                'title': 'Jazz Love',
                'audio_url': '',
                'video_url': 'http://example.com/song3.mp4',
                'created_at': '2025-02-01T00:00:00Z',
                'status': 'processing'
            }
        ]

    def test_filter_by_title(self):
        """Test filtering by title"""
        criteria = {'title': 'love'}
        filtered = self.downloader._apply_filters(self.songs, criteria)

        assert len(filtered) == 2
        assert all('love' in song['title'].lower() for song in filtered)

    def test_filter_by_status(self):
        """Test filtering by status"""
        criteria = {'status': 'complete'}
        filtered = self.downloader._apply_filters(self.songs, criteria)

        assert len(filtered) == 2
        assert all(song['status'] == 'complete' for song in filtered)

    def test_filter_by_has_video(self):
        """Test filtering by has_video"""
        criteria = {'has_video': True}
        filtered = self.downloader._apply_filters(self.songs, criteria)

        assert len(filtered) == 2
        assert all(song['video_url'] for song in filtered)

    def test_filter_by_has_audio(self):
        """Test filtering by has_audio"""
        criteria = {'has_audio': True}
        filtered = self.downloader._apply_filters(self.songs, criteria)

        assert len(filtered) == 2
        assert all(song['audio_url'] for song in filtered)

    def test_filter_by_min_date(self):
        """Test filtering by minimum date"""
        criteria = {'min_date': '2025-01-10T00:00:00+00:00'}
        filtered = self.downloader._apply_filters(self.songs, criteria)

        assert len(filtered) == 2

    def test_filter_by_max_date(self):
        """Test filtering by maximum date"""
        criteria = {'max_date': '2025-01-20T00:00:00+00:00'}
        filtered = self.downloader._apply_filters(self.songs, criteria)

        assert len(filtered) == 2

    def test_filter_combined(self):
        """Test multiple filters combined"""
        criteria = {
            'title': 'love',
            'has_video': True,
            'status': 'complete'
        }
        filtered = self.downloader._apply_filters(self.songs, criteria)

        assert len(filtered) == 1
        assert filtered[0]['id'] == 'song1'


class TestWaitForGeneration:
    """Test waiting for song generation"""

    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    def test_wait_already_complete(self, mock_sleep, mock_chrome):
        """Test when song is already complete"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        downloader = SunoDownloader("user@test.com", "password")
        downloader.setup_driver()

        song = {
            'id': 'song1',
            'title': 'Test Song',
            'status': 'complete'
        }

        result = downloader.wait_for_generation(song)

        assert result['status'] == 'complete'
        mock_sleep.assert_not_called()

    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    @patch('automated_downloader.time.time')
    def test_wait_timeout(self, mock_time, mock_sleep, mock_chrome):
        """Test timeout while waiting"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_driver.execute_script.return_value = []

        # Mock time to trigger timeout
        time_values = [0, 0, 400]
        time_index = [0]

        def get_time():
            result = time_values[time_index[0]]
            time_index[0] = min(time_index[0] + 1, len(time_values) - 1)
            return result

        mock_time.side_effect = get_time

        downloader = SunoDownloader("user@test.com", "password")
        downloader.setup_driver()

        song = {
            'id': 'song1',
            'title': 'Test Song',
            'status': 'processing'
        }

        result = downloader.wait_for_generation(song, max_wait_time=300)

        assert result['status'] == 'processing'


class TestDownloadFile:
    """Test file downloading"""

    @patch('automated_downloader.requests.get')
    def test_download_file_success(self, mock_get):
        """Test successful file download"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock response
            mock_response = MagicMock()
            mock_response.headers.get.return_value = '1024'
            mock_response.iter_content.return_value = [b'test data']
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            downloader = SunoDownloader("user@test.com", "password", download_dir=tmpdir)

            result = downloader.download_file(
                'http://example.com/test.mp3',
                'test.mp3',
                'mp3'
            )

            assert result is True
            assert os.path.exists(os.path.join(tmpdir, 'test.mp3'))

    @patch('automated_downloader.requests.get')
    def test_download_file_already_exists(self, mock_get):
        """Test skipping download when file already exists"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create existing file
            existing_file = os.path.join(tmpdir, 'existing.mp3')
            with open(existing_file, 'w') as f:
                f.write('existing content')

            downloader = SunoDownloader("user@test.com", "password", download_dir=tmpdir)

            result = downloader.download_file(
                'http://example.com/test.mp3',
                'existing.mp3',
                'mp3'
            )

            assert result is True
            mock_get.assert_not_called()

    @patch('automated_downloader.requests.get')
    def test_download_file_no_url(self, mock_get):
        """Test download with empty URL"""
        with tempfile.TemporaryDirectory() as tmpdir:
            downloader = SunoDownloader("user@test.com", "password", download_dir=tmpdir)

            result = downloader.download_file('', 'test.mp3', 'mp3')

            assert result is False
            mock_get.assert_not_called()

    @patch('automated_downloader.requests.get')
    def test_download_file_request_failure(self, mock_get):
        """Test download with request failure"""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_get.side_effect = Exception("Network error")

            downloader = SunoDownloader("user@test.com", "password", download_dir=tmpdir)

            result = downloader.download_file(
                'http://example.com/test.mp3',
                'test.mp3',
                'mp3'
            )

            assert result is False


class TestGetWavUrl:
    """Test WAV URL construction"""

    def test_get_wav_url_with_audio(self):
        """Test WAV URL when audio URL exists"""
        downloader = SunoDownloader("user@test.com", "password")

        song = {
            'audio_url': 'http://example.com/song.mp3'
        }

        wav_url = downloader.get_wav_url(song)

        assert wav_url == 'http://example.com/song.wav'

    def test_get_wav_url_without_audio(self):
        """Test WAV URL when no audio URL"""
        downloader = SunoDownloader("user@test.com", "password")

        song = {
            'audio_url': ''
        }

        wav_url = downloader.get_wav_url(song)

        assert wav_url is None


class TestDownloadSong:
    """Test downloading a complete song"""

    @patch('automated_downloader.requests.get')
    @patch('automated_downloader.webdriver.Chrome')
    def test_download_song_all_formats(self, mock_chrome, mock_get):
        """Test downloading all formats for a song"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock response
            mock_response = MagicMock()
            mock_response.headers.get.return_value = '1024'
            mock_response.iter_content.return_value = [b'test data']
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            mock_driver = MagicMock()
            mock_chrome.return_value = mock_driver

            downloader = SunoDownloader(
                "user@test.com",
                "password",
                download_dir=tmpdir,
                formats=['mp3', 'mp4', 'wav']
            )
            downloader.setup_driver()

            song = {
                'id': 'song1',
                'title': 'Test Song',
                'audio_url': 'http://example.com/song.mp3',
                'video_url': 'http://example.com/song.mp4',
                'status': 'complete'
            }

            results = downloader.download_song(song, wait_for_gen=False)

            assert 'mp3' in results
            assert 'mp4' in results
            assert 'wav' in results
            assert results['mp3'] is True
            assert results['mp4'] is True

    @patch('automated_downloader.requests.get')
    @patch('automated_downloader.webdriver.Chrome')
    def test_download_song_sanitize_filename(self, mock_chrome, mock_get):
        """Test filename sanitization"""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_response = MagicMock()
            mock_response.headers.get.return_value = '1024'
            mock_response.iter_content.return_value = [b'test data']
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            mock_driver = MagicMock()
            mock_chrome.return_value = mock_driver

            downloader = SunoDownloader(
                "user@test.com",
                "password",
                download_dir=tmpdir,
                formats=['mp3']
            )
            downloader.setup_driver()

            song = {
                'id': 'song1',
                'title': 'Test/Song:With*Special|Chars',
                'audio_url': 'http://example.com/song.mp3',
                'video_url': '',
                'status': 'complete'
            }

            downloader.download_song(song, wait_for_gen=False)

            # Check that file was created with sanitized name
            files = os.listdir(tmpdir)
            assert len(files) == 1
            assert '/' not in files[0]
            assert ':' not in files[0]
            assert '*' not in files[0]


class TestRun:
    """Test main run method"""

    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    @patch('automated_downloader.requests.get')
    def test_run_complete_workflow(self, mock_get, mock_sleep, mock_chrome):
        """Test complete workflow"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Setup mocks
            mock_driver = MagicMock()
            mock_chrome.return_value = mock_driver
            mock_driver.current_url = "https://suno.com/songs"

            # Mock login elements
            mock_email_input = MagicMock()
            mock_password_input = MagicMock()
            mock_login_button = MagicMock()

            mock_driver.find_element.side_effect = [
                mock_password_input,
                mock_login_button
            ]

            mock_wait = MagicMock()
            mock_wait.until.return_value = mock_email_input

            # Mock scroll and extract
            call_count = [0]
            def execute_script_handler(script):
                call_count[0] += 1
                if 'scrollHeight' in script:
                    return 1000  # Same height to end scrolling
                elif 'scrollTo' in script:
                    return None
                else:
                    # Extract songs call
                    return [
                        {
                            'id': 'song1',
                            'title': 'Test Song',
                            'audio_url': 'http://example.com/song.mp3',
                            'video_url': 'http://example.com/song.mp4',
                            'created_at': '2025-01-01T00:00:00Z',
                            'duration': 180,
                            'status': 'complete',
                            'tags': []
                        }
                    ]

            mock_driver.execute_script.side_effect = execute_script_handler

            # Mock download
            mock_response = MagicMock()
            mock_response.headers.get.return_value = '1024'
            mock_response.iter_content.return_value = [b'test data']
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            downloader = SunoDownloader(
                "user@test.com",
                "password",
                download_dir=tmpdir,
                formats=['mp3']
            )

            with patch.object(downloader, 'setup_driver'):
                downloader.driver = mock_driver
                downloader.wait = mock_wait
                downloader.run(wait_for_generation=False)

            # Verify driver was quit
            mock_driver.quit.assert_called_once()

    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    def test_run_no_songs(self, mock_sleep, mock_chrome):
        """Test run when no songs are found"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver
        mock_driver.current_url = "https://suno.com/songs"

        mock_email_input = MagicMock()
        mock_password_input = MagicMock()
        mock_login_button = MagicMock()

        mock_driver.find_element.side_effect = [
            mock_password_input,
            mock_login_button
        ]

        mock_wait = MagicMock()
        mock_wait.until.return_value = mock_email_input

        # Mock scroll and empty songs
        def execute_script_handler(script):
            if 'scrollHeight' in script:
                return 1000
            elif 'scrollTo' in script:
                return None
            else:
                return []  # No songs

        mock_driver.execute_script.side_effect = execute_script_handler

        downloader = SunoDownloader("user@test.com", "password")

        with patch.object(downloader, 'setup_driver'):
            downloader.driver = mock_driver
            downloader.wait = mock_wait
            downloader.run()

        # Verify driver was quit
        mock_driver.quit.assert_called_once()

    @patch('automated_downloader.webdriver.Chrome')
    def test_run_handles_exception(self, mock_chrome):
        """Test that run handles exceptions gracefully"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        downloader = SunoDownloader("user@test.com", "password")

        with patch.object(downloader, 'setup_driver'):
            downloader.driver = mock_driver
            with patch.object(downloader, 'login', side_effect=Exception("Test error")):
                with pytest.raises(Exception):
                    downloader.run()

        # Verify driver was still quit
        mock_driver.quit.assert_called_once()


class TestMain:
    """Test main function and CLI argument parsing"""

    @patch('automated_downloader.SunoDownloader')
    @patch('sys.argv', ['automated_downloader.py', '-u', 'test@example.com', '-p', 'password123'])
    def test_main_with_cli_args(self, mock_downloader_class):
        """Test main with command-line arguments"""
        from automated_downloader import main

        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader

        main()

        mock_downloader_class.assert_called_once_with(
            username='test@example.com',
            password='password123',
            download_dir='downloads',
            headless=False,
            formats=['mp3', 'mp4', 'wav']
        )
        mock_downloader.run.assert_called_once()

    @patch('automated_downloader.SunoDownloader')
    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
        "credentials": {
            "username": "config@example.com",
            "password": "configpass"
        },
        "download": {
            "output_dir": "config_downloads",
            "formats": ["mp3", "mp4"]
        },
        "browser": {
            "headless": True
        }
    }))
    @patch('sys.argv', ['automated_downloader.py', '-c', 'config.json'])
    def test_main_with_config_file(self, mock_file, mock_downloader_class):
        """Test main with config file"""
        from automated_downloader import main

        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader

        main()

        mock_downloader_class.assert_called_once()
        call_kwargs = mock_downloader_class.call_args[1]
        assert call_kwargs['username'] == 'config@example.com'
        assert call_kwargs['password'] == 'configpass'

    @patch('sys.argv', ['automated_downloader.py', '-u', 'test@example.com', '-p', 'password', '--filter-title', 'love'])
    @patch('automated_downloader.SunoDownloader')
    def test_main_with_filters(self, mock_downloader_class):
        """Test main with filter arguments"""
        from automated_downloader import main

        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader

        main()

        # Check that run was called with filter criteria
        call_kwargs = mock_downloader.run.call_args[1]
        assert call_kwargs['filter_criteria'] is not None
        assert 'title' in call_kwargs['filter_criteria']
        assert call_kwargs['filter_criteria']['title'] == 'love'

    @patch('sys.argv', ['automated_downloader.py'])
    @patch('sys.exit')
    @patch('automated_downloader.webdriver.Chrome')
    def test_main_missing_credentials(self, mock_chrome, mock_exit):
        """Test main with missing credentials"""
        from automated_downloader import main

        main()

        # Should exit with error
        mock_exit.assert_called_once_with(1)

    @patch('sys.argv', ['automated_downloader.py', '-c', 'nonexistent.json'])
    @patch('sys.exit')
    @patch('automated_downloader.webdriver.Chrome')
    def test_main_invalid_config_file(self, mock_chrome, mock_exit):
        """Test main with invalid config file"""
        from automated_downloader import main

        main()

        # Should exit with error (called with 1)
        assert mock_exit.called
        assert 1 in [call[0][0] for call in mock_exit.call_args_list]
