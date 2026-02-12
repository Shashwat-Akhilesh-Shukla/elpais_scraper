"""
Unit tests for the analyzer module.
"""
import pytest
from collections import Counter
from src.analyzer import WordAnalyzer


class TestWordAnalyzer:
    """Test cases for WordAnalyzer class."""
    
    def test_analyzer_initialization(self):
        """Test analyzer initialization."""
        analyzer = WordAnalyzer(min_occurrences=3)
        assert analyzer.min_occurrences == 3
    
    def test_count_words(self):
        """Test word counting."""
        analyzer = WordAnalyzer()
        headers = [
            "The quick brown fox",
            "The lazy dog",
            "The quick cat"
        ]
        
        word_counts = analyzer.count_words(headers)
        
        assert word_counts["the"] == 3
        assert word_counts["quick"] == 2
        assert word_counts["brown"] == 1
    
    def test_count_words_case_insensitive(self):
        """Test that word counting is case-insensitive."""
        analyzer = WordAnalyzer()
        headers = ["The Dog", "the cat", "THE bird"]
        
        word_counts = analyzer.count_words(headers)
        
        assert word_counts["the"] == 3
    
    def test_filter_repeated_words(self):
        """Test filtering words by minimum occurrences."""
        analyzer = WordAnalyzer(min_occurrences=3)
        word_counts = Counter({"the": 5, "quick": 2, "brown": 1, "fox": 3})
        
        repeated = analyzer.filter_repeated_words(word_counts)
        
        assert "the" in repeated
        assert "fox" in repeated
        assert "quick" not in repeated
        assert "brown" not in repeated
    
    def test_analyze_headers(self):
        """Test full analysis workflow."""
        analyzer = WordAnalyzer(min_occurrences=3)
        headers = [
            "The European Union and the crisis",
            "The political crisis in Europe",
            "European leaders discuss the situation"
        ]
        
        results = analyzer.analyze_headers(headers)
        
        # "the" appears 3 times, "european" appears 2 times
        assert "the" in results
        assert results["the"] == 3
    
    def test_analyze_empty_headers(self):
        """Test analyzing empty headers list."""
        analyzer = WordAnalyzer()
        results = analyzer.analyze_headers([])
        
        assert results == {}
    
    def test_short_words_filtered(self):
        """Test that very short words are filtered out."""
        analyzer = WordAnalyzer()
        headers = ["A big dog is in a box"]
        
        word_counts = analyzer.count_words(headers)
        
        # Single letter words should be filtered
        assert "a" not in word_counts
        assert "big" in word_counts
        assert "dog" in word_counts
