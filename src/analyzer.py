"""
Word frequency analyzer for translated article headers.
"""
import re
from typing import List, Dict, Tuple
from collections import Counter

from src.utils import log_info, log_debug


class WordAnalyzer:
    """
    Analyzer for word frequency in translated headers.
    """
    
    def __init__(self, min_occurrences: int = 3):
        """
        Initialize the analyzer.
        
        Args:
            min_occurrences: Minimum occurrences to consider (words must appear > 2 times)
        """
        self.min_occurrences = min_occurrences
        log_info(f"Word analyzer initialized with min_occurrences: {min_occurrences}")
    
    def count_words(self, headers: List[str]) -> Counter:
        """
        Count word occurrences in headers.
        
        Args:
            headers: List of header texts
            
        Returns:
            Counter object with word frequencies
        """
        log_info(f"Counting words in {len(headers)} headers")
        
        all_words = []
        
        for header in headers:
            # Convert to lowercase for case-insensitive comparison
            header_lower = header.lower()
            
            # Extract words (alphanumeric sequences)
            words = re.findall(r'\b[a-z]+\b', header_lower)
            
            # Filter out very short words (optional, can be adjusted)
            words = [word for word in words if len(word) > 2]
            
            all_words.extend(words)
        
        word_counts = Counter(all_words)
        log_debug(f"Total unique words: {len(word_counts)}")
        
        return word_counts
    
    def filter_repeated_words(self, word_counts: Counter) -> Dict[str, int]:
        """
        Filter words that appear more than the minimum threshold.
        
        Args:
            word_counts: Counter with word frequencies
            
        Returns:
            Dictionary of words with their counts (only words appearing >= min_occurrences)
        """
        # Filter words that appear at least min_occurrences times
        repeated_words = {
            word: count 
            for word, count in word_counts.items() 
            if count >= self.min_occurrences
        }
        
        log_info(f"Found {len(repeated_words)} words appearing {self.min_occurrences}+ times")
        return repeated_words
    
    def analyze_headers(self, translated_headers: List[str]) -> Dict[str, int]:
        """
        Main analysis function.
        
        Args:
            translated_headers: List of translated header texts
            
        Returns:
            Dictionary of repeated words with their counts
        """
        log_info("Starting word frequency analysis")
        
        # Count all words
        word_counts = self.count_words(translated_headers)
        
        # Filter repeated words
        repeated_words = self.filter_repeated_words(word_counts)
        
        # Sort by count (descending)
        sorted_words = dict(sorted(repeated_words.items(), key=lambda x: x[1], reverse=True))
        
        return sorted_words
    
    def print_analysis(self, results: Dict[str, int]) -> None:
        """
        Print analysis results in a formatted way.
        
        Args:
            results: Dictionary of words and their counts
        """
        print("\n" + "="*60)
        print("WORD FREQUENCY ANALYSIS")
        print("="*60)
        print(f"\nWords appearing more than twice (>= {self.min_occurrences} times):\n")
        
        if not results:
            print("No words found appearing more than twice.")
        else:
            # Print in a formatted table
            print(f"{'Word':<20} {'Count':>10}")
            print("-" * 32)
            for word, count in results.items():
                print(f"{word:<20} {count:>10}")
        
        print("\n" + "="*60 + "\n")
