"""
Unit tests for the translator module.
"""
import pytest
from src.translator import ArticleTranslator


class TestArticleTranslator:
    """Test cases for ArticleTranslator class."""
    
    def test_translator_initialization(self):
        """Test translator initialization."""
        translator = ArticleTranslator()
        assert translator.source_lang == "es"
        assert translator.target_lang == "en"
    
    def test_translate_text_spanish_to_english(self):
        """Test translating Spanish text to English."""
        translator = ArticleTranslator()
        spanish_text = "Hola mundo"
        translated = translator.translate_text(spanish_text)
        
        # Should translate to something like "Hello world"
        assert translated.lower() in ["hello world", "hi world", "hello, world"]
    
    def test_translate_empty_text(self):
        """Test translating empty text."""
        translator = ArticleTranslator()
        result = translator.translate_text("")
        assert result == ""
    
    def test_translate_titles_list(self):
        """Test translating a list of titles."""
        translator = ArticleTranslator()
        titles = ["Buenos días", "Buenas noches"]
        translated = translator.translate_titles(titles)
        
        assert len(translated) == 2
        assert all(isinstance(t, str) for t in translated)
    
    def test_get_translated_headers(self):
        """Test extracting and translating headers from articles."""
        translator = ArticleTranslator()
        articles = [
            {"title": "Primera noticia"},
            {"title": "Segunda noticia"}
        ]
        
        results = translator.get_translated_headers(articles)
        
        assert len(results) == 2
        assert all("original" in r and "translated" in r for r in results)
        assert results[0]["original"] == "Primera noticia"
