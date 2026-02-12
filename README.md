# El País Opinion Section Web Scraper

A comprehensive cross-browser web scraper that extracts articles from El País Opinion section, translates headers to English, and analyzes word frequency.

## Features

- **Cross-browser support**: Chrome, Firefox, Edge
- **Mobile device emulation**: Test on mobile viewports
- **Automatic translation**: Spanish to English using Google Translate
- **Image downloading**: Saves article cover images locally
- **Word frequency analysis**: Identifies repeated words in translated headers
- **Comprehensive testing**: Unit and integration tests for all browsers

## Requirements

- Python 3.8 or higher
- Chrome, Firefox, or Edge browser installed
- Internet connection

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd c:\Users\passi\OneDrive\Desktop\Projects\Personal\Job_application_assignments\elpais_scraper
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the scraper with default settings (Chrome browser):

```bash
python main.py
```

### Browser Selection

Choose a specific browser:

```bash
# Chrome (default)
python main.py --browser chrome

# Firefox
python main.py --browser firefox

# Edge
python main.py --browser edge
```

### Headless Mode

Run without opening a browser window:

```bash
python main.py --headless
```

### Mobile Emulation

Emulate a mobile device:

```bash
python main.py --mobile
```

### Combined Options

```bash
python main.py --browser firefox --headless
```

## Output

The scraper will:

1. **Print to console**:
   - Article titles in Spanish
   - Article content snippets in Spanish
   - Translated titles in English
   - Word frequency analysis (words appearing more than twice)

2. **Save images**:
   - Cover images are saved to `output/images/` directory
   - Images are named based on article titles

## Testing

### Run All Tests

```bash
python -m pytest tests/ -v
```

### Run Specific Test Files

```bash
# Unit tests
python -m pytest tests/test_scraper.py -v
python -m pytest tests/test_translator.py -v
python -m pytest tests/test_analyzer.py -v

# Integration tests (cross-browser)
python -m pytest tests/test_integration.py -v
```

### Run Tests for Specific Browser

```bash
python -m pytest tests/test_integration.py::test_chrome_scraping -v
python -m pytest tests/test_integration.py::test_firefox_scraping -v
python -m pytest tests/test_integration.py::test_edge_scraping -v
```

## Project Structure

```
elpais_scraper/
├── src/
│   ├── __init__.py
│   ├── scraper.py          # Main scraper class
│   ├── translator.py       # Translation functionality
│   ├── analyzer.py         # Word frequency analysis
│   └── utils.py            # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_scraper.py     # Scraper unit tests
│   ├── test_translator.py  # Translator unit tests
│   ├── test_analyzer.py    # Analyzer unit tests
│   └── test_integration.py # Cross-browser integration tests
├── output/
│   └── images/             # Downloaded article images
├── config.py               # Configuration settings
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Configuration

Edit `config.py` to customize:

- Number of articles to scrape (default: 5)
- Browser window size
- Timeout settings
- Output directories
- Translation languages

## Troubleshooting

### WebDriver Issues

If you encounter WebDriver errors:

1. The `webdriver-manager` package automatically downloads the correct driver
2. Ensure your browser is up to date
3. Try running with `--headless` flag

### Translation Errors

If translation fails:

1. Check your internet connection
2. The googletrans library may have rate limits - add delays between requests
3. Consider using an alternative translation API

### Image Download Failures

If images don't download:

1. Check the `output/images/` directory exists
2. Verify internet connection
3. Some articles may not have cover images

## License

This project is for educational purposes only.

## Author

Created as part of a job application assignment.
