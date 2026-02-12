"""
Main entry point for El País Opinion Section Web Scraper.
"""
import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from src.scraper import ElPaisScraper
from src.translator import ArticleTranslator
from src.analyzer import WordAnalyzer
from src.utils import log_info, log_error, truncate_text


def print_separator(char="=", length=80):
    """Print a separator line."""
    print(char * length)


def print_articles(articles):
    """Print article information."""
    print_separator()
    print("SCRAPED ARTICLES (Spanish)")
    print_separator()
    
    for i, article in enumerate(articles, 1):
        print(f"\n[Article {i}]")
        print(f"Title: {article['title']}")
        print(f"Content: {truncate_text(article['content'], 300)}")
        print(f"Image URL: {article.get('image_url', 'No image')}")
        print(f"URL: {article['url']}")
        print("-" * 80)


def print_translations(translations):
    """Print translated headers."""
    print_separator()
    print("TRANSLATED HEADERS (English)")
    print_separator()
    
    for i, trans in enumerate(translations, 1):
        print(f"\n[{i}] Original (ES): {trans['original']}")
        print(f"    Translated (EN): {trans['translated']}")


def main():
    """Main function."""
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="El País Opinion Section Web Scraper"
    )
    parser.add_argument(
        "--browser",
        choices=["chrome", "firefox", "edge"],
        default="chrome",
        help="Browser to use (default: chrome)"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run in headless mode"
    )
    parser.add_argument(
        "--mobile",
        action="store_true",
        help="Emulate mobile device"
    )
    
    args = parser.parse_args()
    
    print_separator("=")
    print("EL PAÍS OPINION SECTION WEB SCRAPER")
    print_separator("=")
    print(f"\nConfiguration:")
    print(f"  Browser: {args.browser}")
    print(f"  Headless: {args.headless}")
    print(f"  Mobile: {args.mobile}")
    print(f"  Articles to scrape: {config.NUM_ARTICLES}")
    print(f"  Output directory: {config.IMAGES_DIR}")
    print()
    
    try:
        # Step 1: Scrape articles
        log_info("Step 1: Scraping articles from El País Opinion section")
        with ElPaisScraper(browser=args.browser, headless=args.headless, mobile=args.mobile) as scraper:
            articles = scraper.scrape_all()
        
        if not articles:
            log_error("No articles were scraped. Exiting.")
            return 1
        
        # Print scraped articles
        print_articles(articles)
        
        # Step 2: Translate headers
        log_info("\nStep 2: Translating article headers to English")
        translator = ArticleTranslator(
            source_lang=config.TRANSLATION_SOURCE,
            target_lang=config.TRANSLATION_TARGET
        )
        
        translations = translator.get_translated_headers(articles)
        
        # Print translations
        print_translations(translations)
        
        # Step 3: Analyze word frequency
        log_info("\nStep 3: Analyzing word frequency in translated headers")
        analyzer = WordAnalyzer(min_occurrences=config.MIN_WORD_OCCURRENCES)
        
        translated_headers = [t['translated'] for t in translations]
        word_analysis = analyzer.analyze_headers(translated_headers)
        
        # Print analysis
        analyzer.print_analysis(word_analysis)
        
        # Summary
        print_separator("=")
        print("SUMMARY")
        print_separator("=")
        print(f"✓ Successfully scraped {len(articles)} articles")
        print(f"✓ Translated {len(translations)} headers")
        print(f"✓ Found {len(word_analysis)} words appearing 3+ times")
        print(f"✓ Images saved to: {config.IMAGES_DIR}")
        print_separator("=")
        
        log_info("Scraping completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        log_info("\nScraping interrupted by user")
        return 1
    except Exception as e:
        log_error(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
