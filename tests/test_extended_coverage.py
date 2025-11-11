"""
Additional comprehensive tests to achieve 100% coverage
"""

import os
import sys
import tempfile
import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from automated_downloader import SunoDownloader


class TestFiltersExtended:
    """Extended filter tests for edge cases"""

    def setup_method(self):
        """Setup test data"""
        self.downloader = SunoDownloader("user@test.com", "password")
        self.songs = [
            {
                'id': 'song1',
                'title': 'Song With Video',
                'audio_url': 'http://example.com/song1.mp3',
                'video_url': 'http://example.com/song1.mp4',
                'created_at': '2025-01-01T00:00:00Z',
                'status': 'complete'
            },
            {
                'id': 'song2',
                'title': 'Song No Video',
                'audio_url': 'http://example.com/song2.mp3',
                'video_url': '',
                'created_at': '2025-01-15T00:00:00Z',
                'status': 'complete'
            }
        ]

    def test_filter_has_video_false(self):
        """Test filtering songs without video"""
        criteria = {'has_video': False}
        filtered = self.downloader._apply_filters(self.songs, criteria)

        assert len(filtered) == 1
        assert filtered[0]['id'] == 'song2'

    def test_filter_has_audio_false(self):
        """Test filtering songs without audio"""
        songs = [
            {
                'id': 'song1',
                'title': 'With Audio',
                'audio_url': 'http://example.com/song1.mp3',
                'video_url': ''
            },
            {
                'id': 'song2',
                'title': 'No Audio',
                'audio_url': '',
                'video_url': 'http://example.com/song2.mp4'
            }
        ]
        criteria = {'has_audio': False}
        filtered = self.downloader._apply_filters(songs, criteria)

        assert len(filtered) == 1
        assert filtered[0]['id'] == 'song2'

    @patch('automated_downloader.webdriver.Chrome')
    def test_extract_songs_with_filters(self, mock_chrome):
        """Test extracting songs with filter criteria"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        # Mock JavaScript execution
        mock_driver.execute_script.return_value = [
            {'id': 'song1', 'title': 'Love Song', 'status': 'complete'},
            {'id': 'song2', 'title': 'Rock Song', 'status': 'complete'}
        ]

        downloader = SunoDownloader("user@test.com", "password")
        downloader.setup_driver()

        filter_criteria = {'title': 'love'}
        songs = downloader.extract_songs_data(filter_criteria)

        assert len(songs) == 1
        assert songs[0]['title'] == 'Love Song'


class TestWaitForGenerationExtended:
    """Extended wait for generation tests"""

    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    @patch('automated_downloader.time.time')
    def test_wait_for_generation_updates_and_completes(self, mock_time, mock_sleep, mock_chrome):
        """Test waiting with song status updating to complete"""
        mock_driver = MagicMock()
        mock_chrome.return_value = mock_driver

        # Mock time to not trigger timeout
        time_values = [0, 0, 5, 10, 15]
        time_index = [0]

        def get_time():
            result = time_values[min(time_index[0], len(time_values) - 1)]
            time_index[0] += 1
            return result

        mock_time.side_effect = get_time

        # First call returns processing, second returns complete
        mock_driver.execute_script.side_effect = [
            [{'id': 'song1', 'title': 'Test', 'status': 'processing'}],
            [{'id': 'song1', 'title': 'Test', 'status': 'complete'}]
        ]

        downloader = SunoDownloader("user@test.com", "password")
        downloader.setup_driver()

        song = {'id': 'song1', 'title': 'Test', 'status': 'processing'}

        result = downloader.wait_for_generation(song, max_wait_time=300)

        assert result['status'] == 'complete'


class TestDownloadFileExtended:
    """Extended download file tests"""

    @patch('automated_downloader.requests.get')
    def test_download_large_file_progress(self, mock_get):
        """Test downloading large file with progress logging"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create multiple chunks that add up to > 1MB to trigger progress logging
            chunk_size = 1024 * 1024  # Exactly 1MB chunk
            chunks = [b'x' * chunk_size, b'y' * chunk_size, b'z' * 100]

            mock_response = MagicMock()
            mock_response.headers.get.return_value = str(sum(len(c) for c in chunks))
            mock_response.iter_content.return_value = chunks
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            downloader = SunoDownloader("user@test.com", "password", download_dir=tmpdir)

            result = downloader.download_file(
                'http://example.com/large.mp3',
                'large.mp3',
                'mp3'
            )

            assert result is True

    @patch('automated_downloader.requests.get')
    def test_download_file_cleanup_on_error(self, mock_get):
        """Test that partial files are cleaned up on error"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock request to fail mid-download
            mock_response = MagicMock()
            mock_response.headers.get.return_value = '1000'
            mock_response.iter_content.side_effect = Exception("Connection lost")
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            downloader = SunoDownloader("user@test.com", "password", download_dir=tmpdir)

            # File doesn't exist yet
            test_file = Path(tmpdir) / 'test.mp3'
            assert not test_file.exists()

            result = downloader.download_file(
                'http://example.com/test.mp3',
                'test.mp3',
                'mp3'
            )

            assert result is False
            # File should not exist after cleanup
            assert not test_file.exists()

    @patch('automated_downloader.requests.get')
    def test_download_file_with_empty_chunks(self, mock_get):
        """Test downloading file with some empty chunks"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock response with mix of empty and non-empty chunks
            chunks = [b'data1', b'', b'data2', None, b'data3']

            mock_response = MagicMock()
            mock_response.headers.get.return_value = '15'
            mock_response.iter_content.return_value = chunks
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            downloader = SunoDownloader("user@test.com", "password", download_dir=tmpdir)

            result = downloader.download_file(
                'http://example.com/test.mp3',
                'test.mp3',
                'mp3'
            )

            assert result is True


class TestDownloadSongExtended:
    """Extended download song tests"""

    @patch('automated_downloader.requests.get')
    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    @patch('automated_downloader.time.time')
    def test_download_song_with_generation_wait(self, mock_time, mock_sleep, mock_chrome, mock_get):
        """Test downloading song that needs generation wait"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock time
            time_values = [0, 0, 5]
            time_index = [0]

            def get_time():
                result = time_values[min(time_index[0], len(time_values) - 1)]
                time_index[0] += 1
                return result

            mock_time.side_effect = get_time

            # Mock driver and song data
            mock_driver = MagicMock()
            mock_chrome.return_value = mock_driver
            mock_driver.execute_script.return_value = [
                {'id': 'song1', 'title': 'Test', 'status': 'complete',
                 'audio_url': 'http://example.com/test.mp3'}
            ]

            # Mock download
            mock_response = MagicMock()
            mock_response.headers.get.return_value = '1024'
            mock_response.iter_content.return_value = [b'test data']
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            downloader = SunoDownloader("user@test.com", "password",
                                       download_dir=tmpdir, formats=['mp3'])
            downloader.setup_driver()

            song = {
                'id': 'song1',
                'title': 'Test',
                'status': 'processing',
                'audio_url': 'http://example.com/test.mp3'
            }

            results = downloader.download_song(song, wait_for_gen=True)

            assert 'mp3' in results

    @patch('automated_downloader.requests.get')
    @patch('automated_downloader.webdriver.Chrome')
    def test_download_song_with_all_formats(self, mock_chrome, mock_get):
        """Test downloading song with all three formats"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Mock driver
            mock_driver = MagicMock()
            mock_chrome.return_value = mock_driver

            # Mock download
            mock_response = MagicMock()
            mock_response.headers.get.return_value = '1024'
            mock_response.iter_content.return_value = [b'test data']
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            downloader = SunoDownloader("user@test.com", "password",
                                       download_dir=tmpdir,
                                       formats=['mp3', 'mp4', 'wav'])
            downloader.setup_driver()

            song = {
                'id': 'song1',
                'title': 'Test',
                'status': 'complete',
                'audio_url': 'http://example.com/test.mp3',
                'video_url': 'http://example.com/test.mp4'
            }

            results = downloader.download_song(song, wait_for_gen=False)

            assert 'mp3' in results
            assert 'mp4' in results
            assert 'wav' in results


class TestRunExtended:
    """Extended run method tests"""

    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    @patch('automated_downloader.requests.get')
    def test_run_with_failed_downloads(self, mock_get, mock_sleep, mock_chrome):
        """Test run with some failed downloads"""
        with tempfile.TemporaryDirectory() as tmpdir:
            mock_driver = MagicMock()
            mock_chrome.return_value = mock_driver
            mock_driver.current_url = "https://suno.com/songs"

            # Setup login mocks
            mock_email_input = MagicMock()
            mock_password_input = MagicMock()
            mock_login_button = MagicMock()

            mock_driver.find_element.side_effect = [
                mock_password_input,
                mock_login_button
            ]

            mock_wait = MagicMock()
            mock_wait.until.return_value = mock_email_input

            # Mock scroll and songs with no URLs (will fail download)
            def execute_script_handler(script):
                if 'scrollHeight' in script:
                    return 1000
                elif 'scrollTo' in script:
                    return None
                else:
                    return [
                        {
                            'id': 'song1',
                            'title': 'Test Song',
                            'audio_url': '',  # No URL = will fail
                            'video_url': '',
                            'status': 'complete'
                        }
                    ]

            mock_driver.execute_script.side_effect = execute_script_handler

            downloader = SunoDownloader("user@test.com", "password",
                                       download_dir=tmpdir, formats=['mp3'])

            with patch.object(downloader, 'setup_driver'):
                downloader.driver = mock_driver
                downloader.wait = mock_wait
                downloader.run()

            mock_driver.quit.assert_called_once()

    @patch('automated_downloader.webdriver.Chrome')
    @patch('automated_downloader.time.sleep')
    def test_run_with_song_processing_error(self, mock_sleep, mock_chrome):
        """Test run when song processing raises exception"""
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

        def execute_script_handler(script):
            if 'scrollHeight' in script:
                return 1000
            elif 'scrollTo' in script:
                return None
            else:
                return [{'id': 'song1', 'title': 'Test', 'status': 'complete'}]

        mock_driver.execute_script.side_effect = execute_script_handler

        downloader = SunoDownloader("user@test.com", "password")

        # Mock download_song to raise exception
        with patch.object(downloader, 'setup_driver'):
            downloader.driver = mock_driver
            downloader.wait = mock_wait
            with patch.object(downloader, 'download_song', side_effect=Exception("Test error")):
                downloader.run()

        mock_driver.quit.assert_called_once()


class TestMainConfigFilters:
    """Test main function with config file filters"""

    @patch('automated_downloader.SunoDownloader')
    @patch('builtins.open', new_callable=MagicMock)
    @patch('sys.argv', ['automated_downloader.py', '-c', 'config.json'])
    def test_main_with_config_filters(self, mock_file, mock_downloader_class):
        """Test main with config file containing filters"""
        import json

        config_data = {
            "credentials": {"username": "test@example.com", "password": "pass"},
            "download": {"output_dir": "downloads", "formats": ["mp3"]},
            "browser": {"headless": False},
            "filters": {
                "title": "love",
                "status": "complete",
                "has_video": True,
                "has_audio": True,
                "min_date": "2025-01-01",
                "max_date": "2025-12-31"
            }
        }

        mock_file.return_value.__enter__.return_value.read.return_value = json.dumps(config_data)

        mock_downloader = MagicMock()
        mock_downloader_class.return_value = mock_downloader

        from automated_downloader import main
        main()

        # Verify filters were applied
        call_kwargs = mock_downloader.run.call_args[1]
        assert call_kwargs['filter_criteria'] is not None
        assert 'title' in call_kwargs['filter_criteria']
        assert 'status' in call_kwargs['filter_criteria']
        assert 'has_video' in call_kwargs['filter_criteria']
        assert 'has_audio' in call_kwargs['filter_criteria']
        assert 'min_date' in call_kwargs['filter_criteria']
        assert 'max_date' in call_kwargs['filter_criteria']
