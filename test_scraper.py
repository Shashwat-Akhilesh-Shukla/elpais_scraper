"""
Pytest tests for El País scraper with BrowserStack parallel execution.
Uses pytest parametrization to run across 5 different platforms in parallel.
"""
import pytest
import os
from pathlib import Path
from selenium import webdriver

# Add src to path
import sys
sys.path.insert(0, str(Path(__file__).parent))

import config
from src.scraper import ElPaisScraper
from src.translator import ArticleTranslator
from src.analyzer import WordAnalyzer
from src.utils import log_info, log_error

# BrowserStack credentials
USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

# Define 5 platform configurations
PLATFORMS = [
    {
        "name": "Windows 11 - Chrome",
        "browserName": "Chrome",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "11",
            "projectName": "BrowserStack Assignment",
            "buildName": "El Pais Selenium Build - Parallel",
            "sessionName": "Desktop - Windows 11 Chrome"
        }
    },
    {
        "name": "macOS Ventura - Safari",
        "browserName": "Safari",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "OS X",
            "osVersion": "Ventura",
            "projectName": "BrowserStack Assignment",
            "buildName": "El Pais Selenium Build - Parallel",
            "sessionName": "Desktop - macOS Ventura Safari"
        }
    },
    {
        "name": "Windows 10 - Edge",
        "browserName": "Edge",
        "browserVersion": "latest",
        "bstack:options": {
            "os": "Windows",
            "osVersion": "10",
            "projectName": "BrowserStack Assignment",
            "buildName": "El Pais Selenium Build - Parallel",
            "sessionName": "Desktop - Windows 10 Edge"
        }
    },
    {
        "name": "iPhone 14 - Safari",
        "browserName": "Safari",
        "bstack:options": {
            "deviceName": "iPhone 14",
            "osVersion": "16",
            "projectName": "BrowserStack Assignment",
            "buildName": "El Pais Selenium Build - Parallel",
            "sessionName": "Mobile - iPhone 14 Safari"
        }
    },
    {
        "name": "Samsung Galaxy S23 - Chrome",
        "browserName": "Chrome",
        "bstack:options": {
            "deviceName": "Samsung Galaxy S23",
            "osVersion": "13.0",
            "projectName": "BrowserStack Assignment",
            "buildName": "El Pais Selenium Build - Parallel",
            "sessionName": "Mobile - Samsung Galaxy S23 Chrome"
        }
    }
]


@pytest.fixture(params=PLATFORMS, ids=[p["name"] for p in PLATFORMS])
def driver(request):
    """
    Fixture to create BrowserStack Remote WebDriver for each platform.
    Runs in parallel using pytest-xdist.
    """
    platform = request.param
    
    if not USERNAME or not ACCESS_KEY:
        pytest.skip("BrowserStack credentials not found")
    
    log_info(f"Creating driver for: {platform['name']}")
    
    # Create options
    options = webdriver.ChromeOptions()
    for key, value in platform.items():
        if key != "name":
            options.set_capability(key, value)
    
    # Create Remote WebDriver
    driver = webdriver.Remote(
        command_executor=f"https://{USERNAME}:{ACCESS_KEY}@hub.browserstack.com/wd/hub",
        options=options
    )
    
    log_info(f"Driver created successfully for: {platform['name']}")
    
    yield driver
    
    # Mark test status on BrowserStack
    try:
        # Check if test passed or failed
        if hasattr(request.node, 'rep_call') and request.node.rep_call.failed:
            # Test failed
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Test failed"}}')
        else:
            # Test passed
            driver.execute_script('browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Test passed successfully"}}')
    except Exception as e:
        log_error(f"Failed to set BrowserStack status: {e}")
    
    # Cleanup
    try:
        driver.quit()
        log_info(f"Driver closed for: {platform['name']}")
    except:
        pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for BrowserStack status reporting."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)



class TestElPaisScraper:
    """Test class for El País scraper with BrowserStack parallel execution."""
    
    def test_scrape_articles(self, driver):
        """Test scraping articles from El País Opinion section."""
        caps = driver.capabilities
        platform_name = caps.get('bstack:options', {}).get('sessionName', 'Unknown')
        
        log_info("=" * 80)
        log_info(f"Running test on: {platform_name}")
        log_info("=" * 80)
        
        # Create scraper with BrowserStack driver
        scraper = ElPaisScraper(driver=driver)
        
        # Step 1: Navigate and scrape articles
        log_info("Step 1: Scraping articles")
        assert scraper.navigate_to_opinion(), "Failed to navigate to Opinion section"
        
        article_links = scraper.get_article_links(config.NUM_ARTICLES)
        assert len(article_links) > 0, "No article links found"
        log_info(f"Found {len(article_links)} article links")
        
        # Scrape articles (limit to 3 for faster execution)
        articles = []
        for i, link in enumerate(article_links[:3], 1):
            log_info(f"Scraping article {i}/3")
            article_data = scraper.scrape_article(link)
            if article_data:
                articles.append(article_data)
        
        assert len(articles) > 0, "No articles were scraped"
        log_info(f"Successfully scraped {len(articles)} articles")
        
        # Step 2: Translate headers
        log_info("Step 2: Translating headers")
        translator = ArticleTranslator(
            source_lang=config.TRANSLATION_SOURCE,
            target_lang=config.TRANSLATION_TARGET
        )
        translations = translator.get_translated_headers(articles)
        assert len(translations) == len(articles), "Translation count mismatch"
        log_info(f"Successfully translated {len(translations)} headers")
        
        # Print translations
        for i, trans in enumerate(translations, 1):
            log_info(f"[{i}] {trans['original']} -> {trans['translated']}")
        
        # Step 3: Analyze word frequency
        log_info("Step 3: Analyzing word frequency")
        analyzer = WordAnalyzer(min_occurrences=2)
        translated_headers = [t['translated'] for t in translations]
        word_analysis = analyzer.analyze_headers(translated_headers)
        log_info(f"Found {len(word_analysis)} words appearing 2+ times")
        
        # Assertions
        assert all('title' in article for article in articles), "Missing titles in articles"
        assert all('content' in article for article in articles), "Missing content in articles"
        assert all('translated' in trans for trans in translations), "Missing translations"
        
        log_info("=" * 80)
        log_info(f"TEST PASSED on {platform_name}")
        log_info("=" * 80)


if __name__ == "__main__":
    # Run with pytest-xdist for parallel execution
    pytest.main([__file__, "-v", "-s", "-n", "5", "--html=report.html", "--self-contained-html"])
