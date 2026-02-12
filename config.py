"""
Configuration settings for El País web scraper.
"""
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent

# URLs
BASE_URL = "https://elpais.com"
OPINION_URL = "https://elpais.com/opinion/"

# Scraping settings
NUM_ARTICLES = 5
LANGUAGE = "es"  # Spanish

# Output directories
OUTPUT_DIR = BASE_DIR / "output"
IMAGES_DIR = OUTPUT_DIR / "images"

# Create output directories if they don't exist
OUTPUT_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)

# Browser settings
BROWSER_OPTIONS = {
    "headless": False,
    "window_size": (1920, 1080),
    "disable_gpu": True,
    "no_sandbox": True,
    "disable_dev_shm_usage": True,
}

# Mobile emulation settings
MOBILE_EMULATION = {
    "deviceName": "iPhone 12 Pro"
}

# Timeout settings (in seconds)
PAGE_LOAD_TIMEOUT = 30
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15

# Translation settings
TRANSLATION_SOURCE = "es"
TRANSLATION_TARGET = "en"

# Word analysis settings
MIN_WORD_OCCURRENCES = 3  # Words must appear more than twice (i.e., >= 3 times)

# Logging
LOG_LEVEL = "INFO"
