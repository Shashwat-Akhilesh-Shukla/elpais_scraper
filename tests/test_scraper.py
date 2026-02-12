"""
Unit tests for the scraper module.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.scraper import ElPaisScraper


class TestElPaisScraper:
    """Test cases for ElPaisScraper class."""
    
    @patch('src.scraper.ChromeDriverManager')
    @patch('src.scraper.webdriver.Chrome')
    def test_scraper_initialization_chrome(self, mock_chrome, mock_driver_manager):
        """Test scraper initialization with Chrome."""
        mock_driver_manager.return_value.install.return_value = "/path/to/chromedriver"
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        scraper = ElPaisScraper(browser="chrome")
        
        assert scraper.browser_name == "chrome"
        assert scraper.driver is not None
        
        scraper.close()
    
    @patch('src.scraper.GeckoDriverManager')
    @patch('src.scraper.webdriver.Firefox')
    def test_scraper_initialization_firefox(self, mock_firefox, mock_driver_manager):
        """Test scraper initialization with Firefox."""
        mock_driver_manager.return_value.install.return_value = "/path/to/geckodriver"
        mock_driver = Mock()
        mock_firefox.return_value = mock_driver
        
        scraper = ElPaisScraper(browser="firefox")
        
        assert scraper.browser_name == "firefox"
        assert scraper.driver is not None
        
        scraper.close()
    
    @patch('src.scraper.EdgeChromiumDriverManager')
    @patch('src.scraper.webdriver.Edge')
    def test_scraper_initialization_edge(self, mock_edge, mock_driver_manager):
        """Test scraper initialization with Edge."""
        mock_driver_manager.return_value.install.return_value = "/path/to/edgedriver"
        mock_driver = Mock()
        mock_edge.return_value = mock_driver
        
        scraper = ElPaisScraper(browser="edge")
        
        assert scraper.browser_name == "edge"
        assert scraper.driver is not None
        
        scraper.close()
    
    def test_invalid_browser(self):
        """Test that invalid browser raises error."""
        with pytest.raises(ValueError):
            scraper = ElPaisScraper(browser="invalid")
    
    @patch('src.scraper.ChromeDriverManager')
    @patch('src.scraper.webdriver.Chrome')
    def test_sanitize_filename(self, mock_chrome, mock_driver_manager):
        """Test filename sanitization."""
        from src.utils import sanitize_filename
        
        # Test with special characters
        result = sanitize_filename("Test: Article / Title?")
        assert "/" not in result
        assert ":" not in result
        assert "?" not in result
        
        # Test with spaces
        result = sanitize_filename("Test Article Title")
        assert " " not in result
        assert "_" in result
    
    @patch('src.scraper.ChromeDriverManager')
    @patch('src.scraper.webdriver.Chrome')
    def test_context_manager(self, mock_chrome, mock_driver_manager):
        """Test using scraper as context manager."""
        mock_driver_manager.return_value.install.return_value = "/path/to/chromedriver"
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        with ElPaisScraper(browser="chrome") as scraper:
            assert scraper.driver is not None
        
        # Driver should be closed after context manager exits
        mock_driver.quit.assert_called_once()
