"""
Utility functions for the El País web scraper.
"""
import os
import re
import logging
from pathlib import Path
from typing import Optional
import requests
from PIL import Image
from io import BytesIO

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def sanitize_filename(text: str, max_length: int = 100) -> str:
    """
    Create a safe filename from text.
    
    Args:
        text: Text to convert to filename
        max_length: Maximum length of filename
        
    Returns:
        Safe filename string
    """
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '', text)
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Remove multiple underscores
    filename = re.sub(r'_+', '_', filename)
    # Trim to max length
    filename = filename[:max_length]
    # Remove leading/trailing underscores
    filename = filename.strip('_')
    return filename


def ensure_directory(path: Path) -> None:
    """
    Create directory if it doesn't exist.
    
    Args:
        path: Path to directory
    """
    path.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {path}")


def download_image(url: str, save_path: Path) -> bool:
    """
    Download and save an image from URL.
    
    Args:
        url: Image URL
        save_path: Path to save the image
        
    Returns:
        True if successful, False otherwise
    """
    try:
        logger.info(f"Downloading image from: {url}")
        
        # Send GET request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Open and save image
        image = Image.open(BytesIO(response.content))
        
        # Ensure parent directory exists
        ensure_directory(save_path.parent)
        
        # Save image
        image.save(save_path)
        logger.info(f"Image saved to: {save_path}")
        return True
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download image from {url}: {e}")
        return False
    except Exception as e:
        logger.error(f"Failed to save image to {save_path}: {e}")
        return False


def log_info(message: str) -> None:
    """
    Log an info message.
    
    Args:
        message: Message to log
    """
    logger.info(message)


def log_error(message: str) -> None:
    """
    Log an error message.
    
    Args:
        message: Message to log
    """
    logger.error(message)


def log_debug(message: str) -> None:
    """
    Log a debug message.
    
    Args:
        message: Message to log
    """
    logger.debug(message)


def truncate_text(text: str, max_length: int = 200) -> str:
    """
    Truncate text to a maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
