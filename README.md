# Race Info Scraper

A Python tool to scrape race information (date, name, location) from runningintheusa.com and export to Excel.

## Features

- 🏃 Scrapes race data from runningintheusa.com
- 📅 Supports custom date ranges
- 📄 Automatic pagination (up to 20 pages by default)
- 🤖 Human-like behavior (random delays, rotating user agents)
- 📊 Excel export (.xlsx format)
- 🛑 Intelligent stopping when no more races are found
- 🌐 Three scraping methods: Advanced (undetected), Selenium, and Requests
- 🚀 Session persistence for faster subsequent runs
- 🔄 Cloudflare loop detection and recovery

## Three Scraping Methods

This tool provides three scrapers to handle the website's bot protection:

### 1. **race_scraper_advanced.py** (Undetected ChromeDriver) 🚀 **RECOMMENDED**
- **Most reliable solution for Cloudflare bypass**
- Uses undetected-chromedriver to be completely invisible to bot detection
- Session persistence - saves cookies after first verification
- Auto-detects and handles Cloudflare loops
- Human-like behavior (scrolling, random delays)
- **Best for avoiding endless Cloudflare loops**
- Future runs are faster (uses saved session)

### 2. **race_scraper_selenium.py** (Selenium WebDriver)
- Uses a real Chrome browser with manual verification step
- Opens browser window for you to complete human verification (CAPTCHA/Cloudflare)
- After verification, automatically continues scraping all pages
- Most reliable for websites with strong anti-bot measures
- Good alternative if advanced scraper has issues

### 3. **race_scraper.py** (Requests + CloudScraper)
- Lightweight and fast
- Uses requests library with cloudscraper for bot protection bypass
- Good for servers or environments without a GUI
- **Limitation:** May be blocked by strong bot protection

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. **For Selenium/Advanced scrapers:** Chrome browser must be installed on your system
   - The scraper will automatically download the correct ChromeDriver

## Usage

### Option 1: Advanced Scraper (Recommended - Cloudflare Loop Fix)

Run the advanced scraper with undetected ChromeDriver:

```bash
python race_scraper_advanced.py
```

**How it works:**
1. You'll be prompted to enter date range and settings
2. A Chrome browser window will open (appears like a normal browser)
3. **First run:** You may need to complete verification, then the session is saved
4. **Future runs:** Uses saved cookies to bypass Cloudflare automatically
5. If detected, auto-detects loops and prompts for manual verification
6. Scrapes all pages automatically with human-like behavior

**Key advantages:**
- ✓ Invisible to bot detection (undetected-chromedriver)
- ✓ Session persistence (faster subsequent runs)
- ✓ Loop detection (prevents getting stuck)
- ✓ Human-like scrolling and delays

You'll be prompted to enter:
- Start date (MM-DD-YYYY format)
- End date (MM-DD-YYYY format)
- Maximum pages to scrape (default: 20)
- Output filename (optional)

### Option 2: Selenium Scraper

Run the Selenium-based scraper:

```bash
python race_scraper_selenium.py
```

**How it works:**
1. You'll be prompted to enter date range and settings
2. A Chrome browser window will open automatically
3. You complete any human verification (CAPTCHA/Cloudflare challenge)
4. Press ENTER when you see the race listings
5. The scraper automatically collects data from all pages

You'll be prompted to enter:
- Start date (MM-DD-YYYY format)
- End date (MM-DD-YYYY format)
- Maximum pages to scrape (default: 20)
- Output filename (optional)

### Option 3: Requests Scraper

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

#### Using Advanced Scraper (Recommended):

```python
from race_scraper_advanced import AdvancedRaceScraper

# Use context manager to ensure browser is closed
# First run: may require manual verification (session will be saved)
# Future runs: automatically uses saved session
with AdvancedRaceScraper(headless=False, use_saved_session=True) as scraper:
    # Scrape races (auto-handles Cloudflare)
    races = scraper.scrape_date_range(
        start_date="01-31-2026",
        end_date="02-01-2026",
        max_pages=20
    )

    # Export to Excel
    scraper.export_to_excel(races, "my_races.xlsx")
```

#### Using Selenium Scraper:

```python
from race_scraper_selenium import SeleniumRaceScraper

# Use context manager to ensure browser is closed
# manual_verification=True (default) requires user to complete verification
# headless=False (default) shows browser for manual verification
with SeleniumRaceScraper(headless=False, manual_verification=True) as scraper:
    # Scrape races (will pause for user to complete verification on first page)
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

### Endless Cloudflare Loop / Stuck in "Verifying you are human"
If you keep seeing verification challenges that never complete:
- **This is a common issue with strong bot detection**
- **Solution:** Use `race_scraper_advanced.py` (recommended) - specifically designed to avoid loops
- The advanced scraper uses undetected-chromedriver which is invisible to bot detection
- After first successful verification, it saves your session for future runs
- Includes loop detection to alert you if stuck
- **This is the most reliable method for persistent Cloudflare issues**

### Bot Detection / "Verifying you are human" (First Time)
If you see a verification page (Cloudflare, CAPTCHA):
- **This is expected on first run!** The website uses bot protection
- **Best solution:** Use `race_scraper_advanced.py` - saves your session after verification
- **Alternative:** Use `race_scraper_selenium.py` - requires manual verification each time
- When the browser opens, complete the verification challenge (click checkbox, solve CAPTCHA)
- Press ENTER in the terminal once you see the race listings
- The advanced scraper will save cookies so you don't have to verify again

### 403 Forbidden Error (Requests Scraper)
If you get a 403 error with `race_scraper.py`:
- **Solution:** Use `race_scraper_advanced.py` instead - it bypasses bot detection completely
- The website has strong anti-bot protection that blocks automated requests
- The advanced scraper appears as a real browser to Cloudflare

### Selenium Issues

**"Chrome not found" or driver errors:**
- Make sure Chrome browser is installed
- The webdriver-manager will auto-download the correct ChromeDriver
- If issues persist, manually install ChromeDriver matching your Chrome version

**Selenium runs slowly:**
- This is normal - Selenium loads actual web pages like a real browser
- Average: 3-5 seconds per page with delays

**Browser doesn't open:**
- Check that Chrome is installed
- The scraper runs in visible mode by default (non-headless)
- You need to see the browser to complete manual verification

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
