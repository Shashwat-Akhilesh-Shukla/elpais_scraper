"""
Web scraper for El País Opinion section using Selenium.
"""
import time
from typing import List, Dict, Optional, Tuple
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    NoSuchElementException,
    WebDriverException
)
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

import config
from src.utils import log_info, log_error, log_debug, download_image, sanitize_filename


class ElPaisScraper:
    """
    Web scraper for El País Opinion section.
    """
    
    def __init__(self, browser: str = "chrome", headless: bool = False, mobile: bool = False):
        """
        Initialize the scraper.
        
        Args:
            browser: Browser to use ('chrome', 'firefox', 'edge')
            headless: Run in headless mode
            mobile: Emulate mobile device
        """
        self.browser_name = browser.lower()
        self.headless = headless
        self.mobile = mobile
        self.driver = None
        self.articles_data = []
        
        log_info(f"Initializing scraper with browser: {browser}, headless: {headless}, mobile: {mobile}")
        self._initialize_driver()
    
    def _initialize_driver(self) -> None:
        """Initialize the Selenium WebDriver based on browser choice."""
        try:
            if self.browser_name == "chrome":
                self.driver = self._create_chrome_driver()
            elif self.browser_name == "firefox":
                self.driver = self._create_firefox_driver()
            elif self.browser_name == "edge":
                self.driver = self._create_edge_driver()
            else:
                raise ValueError(f"Unsupported browser: {self.browser_name}")
            
            # Set timeouts
            self.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
            self.driver.implicitly_wait(config.IMPLICIT_WAIT)
            
            log_info(f"{self.browser_name.capitalize()} driver initialized successfully")
            
        except Exception as e:
            log_error(f"Failed to initialize driver: {e}")
            raise
    
    def _create_chrome_driver(self) -> webdriver.Chrome:
        """Create Chrome WebDriver."""
        options = webdriver.ChromeOptions()
        
        if self.headless:
            options.add_argument("--headless=new")
        
        options.add_argument(f"--window-size={config.BROWSER_OPTIONS['window_size'][0]},{config.BROWSER_OPTIONS['window_size'][1]}")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        if self.mobile:
            options.add_experimental_option("mobileEmulation", config.MOBILE_EMULATION)
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _create_firefox_driver(self) -> webdriver.Firefox:
        """Create Firefox WebDriver."""
        options = webdriver.FirefoxOptions()
        
        if self.headless:
            options.add_argument("--headless")
        
        options.set_preference("general.useragent.override", 
                             "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.set_window_size(*config.BROWSER_OPTIONS['window_size'])
        return driver
    
    def _create_edge_driver(self) -> webdriver.Edge:
        """Create Edge WebDriver."""
        options = webdriver.EdgeOptions()
        
        if self.headless:
            options.add_argument("--headless=new")
        
        options.add_argument(f"--window-size={config.BROWSER_OPTIONS['window_size'][0]},{config.BROWSER_OPTIONS['window_size'][1]}")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        
        if self.mobile:
            options.add_experimental_option("mobileEmulation", config.MOBILE_EMULATION)
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    
    def navigate_to_opinion(self) -> bool:
        """
        Navigate to the Opinion section.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            log_info(f"Navigating to: {config.OPINION_URL}")
            self.driver.get(config.OPINION_URL)
            
            # Wait for page to load
            WebDriverWait(self.driver, config.EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.TAG_NAME, "article"))
            )
            
            # Handle cookie consent if present
            self._handle_cookie_consent()
            
            log_info("Successfully navigated to Opinion section")
            return True
            
        except TimeoutException:
            log_error("Timeout waiting for Opinion section to load")
            return False
        except Exception as e:
            log_error(f"Failed to navigate to Opinion section: {e}")
            return False
    
    def _handle_cookie_consent(self) -> None:
        """Handle cookie consent popup if present."""
        try:
            # Common selectors for cookie consent buttons
            consent_selectors = [
                "button[id*='accept']",
                "button[id*='consent']",
                "button.didomi-button",
                "#didomi-notice-agree-button",
                "button[aria-label*='Accept']",
            ]
            
            for selector in consent_selectors:
                try:
                    button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    button.click()
                    log_info("Accepted cookie consent")
                    time.sleep(1)
                    return
                except:
                    continue
                    
        except Exception as e:
            log_debug(f"No cookie consent found or already accepted: {e}")
    
    def get_article_links(self, count: int = 5) -> List[str]:
        """
        Get article links from the Opinion section.
        
        Args:
            count: Number of articles to retrieve
            
        Returns:
            List of article URLs
        """
        try:
            log_info(f"Extracting {count} article links")
            
            # Find all article links
            article_links = []
            
            # Try multiple selectors
            selectors = [
                "article a[href*='/opinion/']",
                "a[href*='/opinion/2026']",
                ".c_h a[href*='/opinion/']",
            ]
            
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for element in elements:
                        href = element.get_attribute("href")
                        if href and href not in article_links and "/opinion/2026" in href:
                            article_links.append(href)
                            if len(article_links) >= count:
                                break
                    
                    if len(article_links) >= count:
                        break
                except:
                    continue
            
            # Remove duplicates and limit to count
            article_links = list(dict.fromkeys(article_links))[:count]
            
            log_info(f"Found {len(article_links)} article links")
            return article_links
            
        except Exception as e:
            log_error(f"Failed to get article links: {e}")
            return []
    
    def scrape_article(self, url: str) -> Optional[Dict[str, str]]:
        """
        Scrape a single article.
        
        Args:
            url: Article URL
            
        Returns:
            Dictionary with article data or None if failed
        """
        try:
            log_info(f"Scraping article: {url}")
            self.driver.get(url)
            
            # Wait for article to load
            WebDriverWait(self.driver, config.EXPLICIT_WAIT).until(
                EC.presence_of_element_located((By.TAG_NAME, "h1"))
            )
            
            time.sleep(2)  # Allow dynamic content to load
            
            # Extract title
            title = self._extract_title()
            
            # Extract content
            content = self._extract_content()
            
            # Extract image URL
            image_url = self._extract_image()
            
            article_data = {
                "url": url,
                "title": title,
                "content": content,
                "image_url": image_url
            }
            
            log_info(f"Successfully scraped article: {title[:50]}...")
            return article_data
            
        except Exception as e:
            log_error(f"Failed to scrape article {url}: {e}")
            return None
    
    def _extract_title(self) -> str:
        """Extract article title."""
        selectors = ["h1", "h1.a_t", ".article_header h1", "header h1"]
        
        for selector in selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                title = element.text.strip()
                if title:
                    return title
            except:
                continue
        
        return "No title found"
    
    def _extract_content(self) -> str:
        """Extract article content."""
        selectors = [
            "article p",
            ".a_c p",
            ".article_body p",
            "div[itemprop='articleBody'] p"
        ]
        
        for selector in selectors:
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                paragraphs = [elem.text.strip() for elem in elements if elem.text.strip()]
                if paragraphs:
                    # Return first few paragraphs
                    return " ".join(paragraphs[:3])
            except:
                continue
        
        return "No content found"
    
    def _extract_image(self) -> Optional[str]:
        """Extract article cover image URL."""
        selectors = [
            "article img",
            ".a_m img",
            "figure img",
            "img[itemprop='image']",
            ".article_header img"
        ]
        
        for selector in selectors:
            try:
                element = self.driver.find_element(By.CSS_SELECTOR, selector)
                src = element.get_attribute("src")
                if src and ("http" in src):
                    return src
            except:
                continue
        
        return None
    
    def scrape_all(self) -> List[Dict[str, str]]:
        """
        Scrape all articles from Opinion section.
        
        Returns:
            List of article data dictionaries
        """
        try:
            # Navigate to Opinion section
            if not self.navigate_to_opinion():
                log_error("Failed to navigate to Opinion section")
                return []
            
            # Get article links
            article_links = self.get_article_links(config.NUM_ARTICLES)
            
            if not article_links:
                log_error("No article links found")
                return []
            
            # Scrape each article
            self.articles_data = []
            for i, link in enumerate(article_links, 1):
                log_info(f"Scraping article {i}/{len(article_links)}")
                article_data = self.scrape_article(link)
                
                if article_data:
                    self.articles_data.append(article_data)
                    
                    # Download image if available
                    if article_data.get("image_url"):
                        filename = sanitize_filename(article_data["title"]) + ".jpg"
                        save_path = config.IMAGES_DIR / filename
                        download_image(article_data["image_url"], save_path)
                
                # Small delay between requests
                time.sleep(1)
            
            log_info(f"Successfully scraped {len(self.articles_data)} articles")
            return self.articles_data
            
        except Exception as e:
            log_error(f"Failed to scrape articles: {e}")
            return []
    
    def close(self) -> None:
        """Close the browser."""
        if self.driver:
            try:
                self.driver.quit()
                log_info("Browser closed")
            except Exception as e:
                log_error(f"Error closing browser: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
