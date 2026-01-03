# Quick Start Guide

Get started scraping race data in 3 simple steps!

## Step 1: Install

```bash
# Install Python dependencies
pip install -r requirements.txt
```

**Note:** Make sure you have Chrome browser installed for the advanced/Selenium scrapers.

## Step 2: Run

### Best Option - Cloudflare Loop Fix (Recommended):

```bash
python race_scraper_advanced.py
```

**Why use this?**
- ✓ Bypasses Cloudflare without getting stuck in loops
- ✓ Saves your session - faster on subsequent runs
- ✓ Auto-detects and handles bot protection

### Alternative Option 1 - Manual Verification:

```bash
python race_scraper_selenium.py
```

### Alternative Option 2 - Lightweight (May be blocked):

```bash
python race_scraper.py
```

## Step 3: Enter Your Details

When prompted, enter:

```
Start date (e.g., 01-31-2026): 01-31-2026
End date (e.g., 02-01-2026): 02-01-2026
Maximum pages to scrape (default 20): 5
Run in headless mode? (Y/n): Y
Output filename (press Enter for auto-generated): my_races.xlsx
```

That's it! Your Excel file will be created with all the race data.

## Expected Output

The tool will:
1. Initialize the browser/scraper
2. Load each page (with human-like delays)
3. Extract race information
4. Save to Excel file

Sample output:
```
Date           Race Name        Location
Jan 31, 2026   Arches Ultra     Moab, UT
Jan 31, 2026   AZT Oracle...    Tucson, AZ
```

## Tips

- **Stuck in Cloudflare loop?** Use `race_scraper_advanced.py` - it's specifically designed to avoid this
- **First run verification:** You may need to verify you're human once, then sessions are saved
- **Start small:** Try 2-3 pages first to test
- **Be patient:** Scraping takes time (2-5 seconds per page)
- **Check dates:** Make sure races exist for your date range on the website
- **Session saved:** After first successful run with advanced scraper, future runs are faster

## Need Help?

- Read the full [README.md](README.md) for detailed documentation
- Check the [Troubleshooting section](README.md#troubleshooting) for common issues
- Look at [example_usage.py](example_usage.py) for code examples
