# Race Info Scraper

A Python tool to scrape race information (date, name, location) from runningintheusa.com and export to Excel.

## Features

- 🏃 Scrapes race data from runningintheusa.com
- 📅 Supports custom date ranges
- 📄 Automatic pagination (up to 20 pages by default)
- 🤖 Human-like behavior (random delays, rotating user agents)
- 📊 Excel export (.xlsx format)
- 🛑 Intelligent stopping when no more races are found
- 🌐 Two scraping methods: Requests-based and Selenium-based

## Two Scraping Methods

This tool provides two scrapers to handle the website's bot protection:

### 1. **race_scraper.py** (Requests + CloudScraper)
- Lightweight and fast
- Uses requests library with cloudscraper for bot protection bypass
- Good for servers or environments without a GUI
- **Limitation:** May be blocked by strong bot protection

### 2. **race_scraper_selenium.py** (Selenium WebDriver) ⭐ **RECOMMENDED**
- Uses a real Chrome browser to bypass bot detection
- More reliable for websites with strong anti-bot measures
- Can run in headless mode (no visible browser window)
- **Best choice for runningintheusa.com**

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **For Selenium scraper:** Chrome browser must be installed on your system
   - The scraper will automatically download the correct ChromeDriver

## Usage

### Option 1: Selenium Scraper (Recommended)

Run the Selenium-based scraper:

```bash
python race_scraper_selenium.py
```

You'll be prompted to enter:
- Start date (MM-DD-YYYY format)
- End date (MM-DD-YYYY format)
- Maximum pages to scrape (default: 20)
- Headless mode (whether to show browser)
- Output filename (optional)

### Option 2: Requests Scraper

Run the requests-based scraper:

```bash
python race_scraper.py
```

You'll be prompted to enter:
- Start date (MM-DD-YYYY format)
- End date (MM-DD-YYYY format)
- Maximum pages to scrape (default: 20)
- Output filename (optional)

### Example

```bash
$ python race_scraper.py

Race Scraper for runningintheusa.com
============================================================

Enter date range in MM-DD-YYYY format
Start date (e.g., 01-31-2026): 01-31-2026
End date (e.g., 02-01-2026): 02-01-2026
Maximum pages to scrape (default 20, press Enter to use default): 5
Output filename (press Enter for auto-generated): my_races.xlsx
```

### Programmatic Usage

#### Using Selenium Scraper (Recommended):

```python
from race_scraper_selenium import SeleniumRaceScraper

# Use context manager to ensure browser is closed
with SeleniumRaceScraper(headless=True) as scraper:
    # Scrape races
    races = scraper.scrape_date_range(
        start_date="01-31-2026",
        end_date="02-01-2026",
        max_pages=20
    )

    # Export to Excel
    scraper.export_to_excel(races, "my_races.xlsx")
```

#### Using Requests Scraper:

```python
from race_scraper import RaceScraper

# Create scraper instance
scraper = RaceScraper()

# Scrape races
races = scraper.scrape_date_range(
    start_date="01-31-2026",
    end_date="02-01-2026",
    max_pages=20
)

# Export to Excel
scraper.export_to_excel(races, "my_races.xlsx")
```

## Output Format

The Excel file will contain three columns:
- **Date**: Race date (e.g., "Jan 31, 2026")
- **Race Name**: Name of the race (e.g., "Arches Ultra")
- **Location**: City and state (e.g., "Moab, UT")

## Human-Like Behavior

To avoid detection and be respectful to the server, the scraper:
- Adds random delays of 2-5 seconds between requests
- Rotates user agents to mimic different browsers
- Uses proper browser headers
- Automatically stops when no more races are found

## Limitations

- Maximum 20 pages per run (configurable, but recommended to prevent excessive scraping)
- Only scrapes 10k to 100m races (as specified in the URL pattern)
- Requires internet connection

## URL Format

The scraper uses URLs in this format:
```
https://runningintheusa.com/classic/list/map/{start-date}-to-{end-date}/10k-to-100m/page-{page}
```

Example:
```
https://runningintheusa.com/classic/list/map/01-31-2026-to-02-01-2026/10k-to-100m/page-1
```

## Troubleshooting

### 403 Forbidden Error (Requests Scraper)
If you get a 403 error with `race_scraper.py`:
- **Solution:** Use `race_scraper_selenium.py` instead - it bypasses bot detection
- The website has strong anti-bot protection that blocks automated requests

### Selenium Issues

**"Chrome not found" or driver errors:**
- Make sure Chrome browser is installed
- The webdriver-manager will auto-download the correct ChromeDriver
- If issues persist, manually install ChromeDriver matching your Chrome version

**Selenium runs slowly:**
- This is normal - Selenium loads actual web pages like a real browser
- Average: 3-5 seconds per page with delays

**Headless mode fails:**
- Try running with headless=False to see the browser
- Some systems have issues with headless Chrome

### General Issues

**No races found:**
- Check that your date range has races listed on runningintheusa.com
- Verify your internet connection
- The website structure may have changed (check HTML parsing logic)
- Try the Selenium scraper if using requests scraper

**Connection errors:**
- Check your internet connection
- The website may be temporarily down
- Increase delay times to avoid rate limiting

## License

MIT License - Feel free to use and modify as needed.
