"""
Translation module using Google Translate API.
"""
import time
from typing import List, Dict
from googletrans import Translator

from src.utils import log_info, log_error, log_debug


class ArticleTranslator:
    """
    Translator for article headers using Google Translate.
    """
    
    def __init__(self, source_lang: str = "es", target_lang: str = "en"):
        """
        Initialize the translator.
        
        Args:
            source_lang: Source language code (default: Spanish)
            target_lang: Target language code (default: English)
        """
        self.translator = Translator()
        self.source_lang = source_lang
        self.target_lang = target_lang
        log_info(f"Translator initialized: {source_lang} -> {target_lang}")
    
    def translate_text(self, text: str, retry_count: int = 3) -> str:
        """
        Translate a single text.
        
        Args:
            text: Text to translate
            retry_count: Number of retries on failure
            
        Returns:
            Translated text or original text if translation fails
        """
        if not text:
            return ""
        
        for attempt in range(retry_count):
            try:
                log_debug(f"Translating: {text[:50]}...")
                result = self.translator.translate(
                    text, 
                    src=self.source_lang, 
                    dest=self.target_lang
                )
                translated = result.text
                log_debug(f"Translated to: {translated[:50]}...")
                return translated
                
            except Exception as e:
                log_error(f"Translation attempt {attempt + 1} failed: {e}")
                if attempt < retry_count - 1:
                    time.sleep(1)  # Wait before retry
                else:
                    log_error(f"All translation attempts failed for: {text[:50]}")
                    return text  # Return original text if all attempts fail
        
        return text
    
    def translate_titles(self, titles: List[str]) -> List[str]:
        """
        Translate a list of titles.
        
        Args:
            titles: List of titles to translate
            
        Returns:
            List of translated titles
        """
        log_info(f"Translating {len(titles)} titles")
        translated_titles = []
        
        for i, title in enumerate(titles, 1):
            log_info(f"Translating title {i}/{len(titles)}")
            translated = self.translate_text(title)
            translated_titles.append(translated)
            
            # Small delay to avoid rate limiting
            if i < len(titles):
                time.sleep(0.5)
        
        log_info(f"Successfully translated {len(translated_titles)} titles")
        return translated_titles
    
    def get_translated_headers(self, articles: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """
        Extract and translate article headers.
        
        Args:
            articles: List of article dictionaries with 'title' key
            
        Returns:
            List of dictionaries with original and translated titles
        """
        log_info(f"Extracting and translating headers from {len(articles)} articles")
        
        results = []
        for article in articles:
            title = article.get("title", "")
            translated_title = self.translate_text(title)
            
            results.append({
                "original": title,
                "translated": translated_title
            })
            
            time.sleep(0.5)  # Rate limiting
        
        return results
