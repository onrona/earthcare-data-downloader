"""
Test suite for EarthCARE Downloader

This module contains unit tests for the EarthCareDownloader class.
"""

import unittest
import os
import tempfile
import pandas as pd
from unittest.mock import Mock, patch, MagicMock
from earthcare_downloader import EarthCareDownloader


class TestEarthCareDownloader(unittest.TestCase):
    """Test cases for EarthCareDownloader class."""

    def setUp(self):
        """Set up test fixtures."""
        self.username = "test_user"
        self.password = "test_password"
        self.downloader = EarthCareDownloader(
            username=self.username,
            password=self.password,
            collection='EarthCAREL1InstChecked',
            verbose=False
        )

    def test_initialization(self):
        """Test downloader initialization."""
        self.assertEqual(self.downloader.username, self.username)
        self.assertEqual(self.downloader.password, self.password)
        self.assertEqual(self.downloader.collection, 'EarthCAREL1InstChecked')
        self.assertFalse(self.downloader.verbose)
        self.assertIsNone(self.downloader.baseline)

    def test_initialization_with_baseline(self):
        """Test downloader initialization with baseline."""
        downloader = EarthCareDownloader(
            username=self.username,
            password=self.password,
            baseline='BA'
        )
        self.assertEqual(downloader.baseline, 'BA')

    def test_detect_csv_separator(self):
        """Test CSV separator detection."""
        # Create temporary CSV files with different separators
        test_data_comma = "date,time,value\n2024-01-01,12:00:00,100"
        test_data_semicolon = "date;time;value\n2024-01-01;12:00:00;100"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(test_data_comma)
            f.flush()
            separator = self.downloader._detect_csv_separator(f.name)
            self.assertEqual(separator, ',')
            os.unlink(f.name)
            
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write(test_data_semicolon)
            f.flush()
            separator = self.downloader._detect_csv_separator(f.name)
            self.assertEqual(separator, ';')
            os.unlink(f.name)

    def test_find_datetime_columns(self):
        """Test datetime column detection."""
        # Test DataFrame with standard column names
        df = pd.DataFrame({
            'date': ['2024-01-01', '2024-01-02'],
            'time': ['12:00:00', '13:00:00'],
            'value': [100, 200]
        })
        
        date_col, time_col = self.downloader._find_datetime_columns(df)
        self.assertEqual(date_col, 'date')
        self.assertEqual(time_col, 'time')

    def test_format_datetime_string(self):
        """Test datetime string formatting."""
        test_datetime = "2024-01-01 12:30:45.123"
        formatted = self.downloader.format_datetime_string(test_datetime)
        self.assertTrue(formatted.endswith('Z'))
        self.assertIn('2024-01-01', formatted)

    def test_string_to_product_name_valid(self):
        """Test valid product name conversion."""
        # Test exact match
        result = self.downloader.string_to_product_name('ATL_NOM_1B')
        self.assertEqual(result, 'ATL_NOM_1B')
        
        # Test short form
        result = self.downloader.string_to_product_name('ANOM')
        self.assertEqual(result, 'ATL_NOM_1B')

    def test_string_to_product_name_invalid(self):
        """Test invalid product name conversion."""
        with self.assertRaises(ValueError):
            self.downloader.string_to_product_name('INVALID_PRODUCT')

    @patch('requests.get')
    def test_get_product_search_template(self, mock_get):
        """Test product search template retrieval."""
        # Mock the first request (OSDD)
        mock_osdd_response = Mock()
        mock_osdd_response.text = '''<?xml version="1.0" encoding="UTF-8"?>
        <OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
            <Url rel="collection" type="application/atom+xml" template="http://test.com/collection?uid={geo:uid}"/>
        </OpenSearchDescription>'''
        
        # Mock the collection request
        mock_collection_response = Mock()
        mock_collection_response.text = '''<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <totalResults xmlns="http://a9.com/-/spec/opensearch/1.1/">1</totalResults>
            <entry>
                <id>test</id>
                <title>Test</title>
                <updated>2024-01-01T00:00:00Z</updated>
                <link rel="search" href="http://test.com/search"/>
            </entry>
        </feed>'''
        
        # Mock the granules OSDD request
        mock_granules_response = Mock()
        mock_granules_response.text = '''<?xml version="1.0" encoding="UTF-8"?>
        <OpenSearchDescription xmlns="http://a9.com/-/spec/opensearch/1.1/">
            <Url rel="results" type="application/atom+xml" template="http://test.com/results?q={searchTerms}"/>
        </OpenSearchDescription>'''
        
        # Configure mock to return different responses for different calls
        mock_get.side_effect = [
            mock_osdd_response,
            mock_collection_response,
            mock_granules_response
        ]
        
        template = self.downloader.get_product_search_template()
        self.assertIn('http://test.com/results', template)

    def test_log_message(self):
        """Test logging functionality."""
        initial_log_count = len(self.downloader.execution_log)
        self.downloader._log("Test message")
        self.assertEqual(len(self.downloader.execution_log), initial_log_count + 1)
        self.assertIn("Test message", self.downloader.execution_log[-1])


class TestGUIImports(unittest.TestCase):
    """Test GUI imports (may fail on headless systems)."""
    
    def test_gui_import(self):
        """Test that GUI can be imported."""
        try:
            from earthcare_downloader_gui import EarthCareDownloaderGUI
            # Just test that we can instantiate the class without running it
            # This might fail on headless systems without display
            self.assertTrue(True)  # If we get here, import worked
        except ImportError:
            self.skipTest("GUI dependencies not available")
        except Exception as e:
            # Expected on headless systems
            if "no display name and no $DISPLAY environment variable" in str(e):
                self.skipTest("No display available for GUI testing")
            else:
                raise


if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)