"""
Integration tests for cross-browser functionality.
"""
import pytest
import time
from pathlib import Path

import config
from src.scraper import ElPaisScraper
from src.translator import ArticleTranslator
from src.analyzer import WordAnalyzer


# Mark all tests as integration tests
pytestmark = pytest.mark.integration


class TestCrossBrowserIntegration:
    """Integration tests for cross-browser scraping."""
    
    @pytest.mark.slow
    def test_chrome_scraping(self):
        """Test full workflow with Chrome browser."""
        with ElPaisScraper(browser="chrome", headless=True) as scraper:
            articles = scraper.scrape_all()
            
            assert len(articles) > 0, "Should scrape at least one article"
            assert len(articles) <= config.NUM_ARTICLES
            
            # Verify article structure
            for article in articles:
                assert "title" in article
                assert "content" in article
                assert "url" in article
                assert len(article["title"]) > 0
    
    @pytest.mark.slow
    def test_firefox_scraping(self):
        """Test full workflow with Firefox browser."""
        with ElPaisScraper(browser="firefox", headless=True) as scraper:
            articles = scraper.scrape_all()
            
            assert len(articles) > 0, "Should scrape at least one article"
            assert len(articles) <= config.NUM_ARTICLES
    
    @pytest.mark.slow
    def test_edge_scraping(self):
        """Test full workflow with Edge browser."""
        with ElPaisScraper(browser="edge", headless=True) as scraper:
            articles = scraper.scrape_all()
            
            assert len(articles) > 0, "Should scrape at least one article"
            assert len(articles) <= config.NUM_ARTICLES
    
    @pytest.mark.slow
    def test_mobile_emulation(self):
        """Test scraping with mobile device emulation."""
        with ElPaisScraper(browser="chrome", headless=True, mobile=True) as scraper:
            articles = scraper.scrape_all()
            
            assert len(articles) > 0, "Should scrape at least one article"
    
    @pytest.mark.slow
    def test_full_workflow(self):
        """Test complete workflow: scrape, translate, analyze."""
        # Step 1: Scrape
        with ElPaisScraper(browser="chrome", headless=True) as scraper:
            articles = scraper.scrape_all()
        
        assert len(articles) > 0, "Should scrape articles"
        
        # Step 2: Translate
        translator = ArticleTranslator()
        translations = translator.get_translated_headers(articles)
        
        assert len(translations) == len(articles)
        assert all("original" in t and "translated" in t for t in translations)
        
        # Step 3: Analyze
        analyzer = WordAnalyzer(min_occurrences=2)  # Lower threshold for testing
        translated_headers = [t["translated"] for t in translations]
        results = analyzer.analyze_headers(translated_headers)
        
        # Results should be a dictionary
        assert isinstance(results, dict)
    
    @pytest.mark.slow
    def test_image_download(self):
        """Test that images are downloaded."""
        with ElPaisScraper(browser="chrome", headless=True) as scraper:
            # Just scrape one article
            if scraper.navigate_to_opinion():
                links = scraper.get_article_links(1)
                if links:
                    article = scraper.scrape_article(links[0])
                    
                    if article and article.get("image_url"):
                        # Check if image was downloaded
                        from src.utils import sanitize_filename, download_image
                        filename = sanitize_filename(article["title"]) + ".jpg"
                        save_path = config.IMAGES_DIR / filename
                        
                        success = download_image(article["image_url"], save_path)
                        
                        if success:
                            assert save_path.exists(), "Image file should exist"
    
    def test_translation_accuracy(self):
        """Test that translation produces reasonable results."""
        translator = ArticleTranslator()
        
        # Test known translations
        test_cases = [
            ("Política", "Politics"),
            ("Economía", "Economy"),
            ("Sociedad", "Society"),
        ]
        
        for spanish, expected_english in test_cases:
            translated = translator.translate_text(spanish)
            # Check if translation is close (case-insensitive)
            assert expected_english.lower() in translated.lower() or \
                   translated.lower() in expected_english.lower()
    
    def test_word_analysis_accuracy(self):
        """Test word frequency analysis accuracy."""
        analyzer = WordAnalyzer(min_occurrences=3)
        
        headers = [
            "The European Union crisis",
            "The political crisis in Europe",
            "European leaders discuss the crisis",
            "The Union responds to crisis"
        ]
        
        results = analyzer.analyze_headers(headers)
        
        # "the" appears 4 times, "crisis" appears 4 times
        assert "the" in results
        assert "crisis" in results
        assert results["the"] >= 3
        assert results["crisis"] >= 3


# Pytest configuration for running specific test groups
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
