# macOS Installation Guide

This guide helps you fix SSL certificate issues and install the race scraper on macOS.

## The SSL Certificate Problem

If you see this error:
```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```

This happens because Python 3.14 on macOS doesn't automatically have SSL certificates configured.

## Quick Fix (Recommended)

### Option 1: Run the Certificate Installer (Easiest)

Python 3.14 comes with a certificate installer. Run this command in Terminal:

```bash
/Applications/Python\ 3.14/Install\ Certificates.command
```

Or navigate to `/Applications/Python 3.14/` in Finder and double-click on `Install Certificates.command`.

### Option 2: Install Using pip (Alternative)

If the above doesn't work, manually install certificates:

```bash
pip3 install --upgrade certifi
```

## Complete Installation Steps

Follow these steps to get the race scraper working:

### 1. Install Python Dependencies

First, navigate to the race-info-getter directory:

```bash
cd /path/to/race-info-getter
```

Then install all required packages:

```bash
pip3 install -r requirements.txt
```

If you get permission errors, try:

```bash
pip3 install --user -r requirements.txt
```

### 2. Install Chrome Browser

The scraper requires Google Chrome. Download and install from:
https://www.google.com/chrome/

### 3. Close All Chrome Windows

Before running the scraper, close all Chrome browser windows to avoid conflicts.

### 4. Run the Scraper

Now you can run the advanced scraper:

```bash
python3 race_scraper_advanced.py
```

## Alternative Scripts

If you still have issues with `race_scraper_advanced.py`, you can use the standard Selenium version:

```bash
python3 race_scraper_selenium.py
```

This uses a different approach that may work better on some systems.

## Troubleshooting

### Error: "Chrome binary not found"

**Solution:** Install Google Chrome from https://www.google.com/chrome/

### Error: "Permission denied"

**Solution:** Try running with `--user` flag:
```bash
pip3 install --user -r requirements.txt
```

### Error: "Module not found"

**Solution:** Make sure you're using the correct Python version:
```bash
python3 --version  # Should show Python 3.14 or similar
pip3 --version     # Should correspond to Python 3.14
```

If they don't match, you may have multiple Python installations. Use:
```bash
python3.14 -m pip install -r requirements.txt
python3.14 race_scraper_advanced.py
```

### Browser opens but gets stuck on Cloudflare

**Solution:** This is normal! When you see the verification page:
1. Wait for any automatic verification to complete (5-10 seconds)
2. Complete any CAPTCHA or checkbox if shown
3. Once you see race listings, press ENTER in the terminal
4. The scraper will save your session for future runs

### SSL error persists after fixing certificates

**Solution:** The new `race_scraper_advanced.py` includes built-in SSL fixes. Make sure you're using the latest version from the repository.

## What Each Script Does

- **race_scraper.py** - Simple requests-based scraper (fastest but may be blocked)
- **race_scraper_selenium.py** - Selenium with manual verification (reliable)
- **race_scraper_advanced.py** - Undetected Chrome (best for Cloudflare bypass)

## Need More Help?

1. Make sure Chrome is installed and updated
2. Close all Chrome windows before running
3. Try running the script multiple times - sometimes it works on the 2nd or 3rd try
4. Check that you have an active internet connection

## Technical Details

The SSL fix works by:
1. Installing `certifi` package with trusted root certificates
2. Configuring Python's SSL context to use these certificates
3. Setting environment variables so `undetected-chromedriver` can download properly

The fix is already built into `race_scraper_advanced.py` (lines 7-11), so you just need to:
1. Install the requirements
2. Run the script
