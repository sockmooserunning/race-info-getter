#!/usr/bin/env python3
"""
Advanced Race Scraper with Cloudflare Bypass and SSL Fix
Uses undetected-chromedriver to bypass bot detection
Includes macOS SSL certificate fix
"""

import ssl
import certifi
import os

# Fix SSL certificate verification on macOS
os.environ['SSL_CERT_FILE'] = certifi.where()
ssl._create_default_https_context = ssl._create_unverified_context

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
from datetime import datetime
from typing import List, Dict
import sys


class AdvancedRaceScraper:
    """Advanced scraper using undetected-chromedriver to bypass Cloudflare"""

    def __init__(self, headless: bool = False, use_saved_session: bool = True):
        """
        Initialize the advanced scraper

        Args:
            headless: Run browser in headless mode (not recommended for Cloudflare)
            use_saved_session: Try to reuse saved cookies from previous session
        """
        print("\n" + "=" * 70)
        print("Advanced Race Scraper - Cloudflare Bypass Edition")
        print("=" * 70)

        self.session_file = "scraper_session.json"
        self.use_saved_session = use_saved_session

        print("\nInitializing undetected Chrome WebDriver...")
        print("This may take a moment on first run...")

        try:
            options = uc.ChromeOptions()

            # Don't use headless mode - Cloudflare detects it
            if headless:
                print("Warning: Headless mode is not recommended for Cloudflare bypass")
                options.add_argument('--headless=new')

            # Add stealth arguments
            options.add_argument('--disable-blink-features=AutomationControlled')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--window-size=1920,1080')

            # Initialize undetected chromedriver with SSL context fix
            self.driver = uc.Chrome(
                options=options,
                version_main=None,  # Auto-detect Chrome version
                use_subprocess=True,
            )

            # Additional stealth
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

            # Try to load saved session
            if use_saved_session and os.path.exists(self.session_file):
                self._load_session()

            print("✓ WebDriver initialized successfully")

        except Exception as e:
            print(f"\n✗ Error initializing driver: {e}")
            print("\nTroubleshooting tips:")
            print("1. Make sure Chrome browser is installed")
            print("2. Close all Chrome instances and try again")
            print("3. Delete any existing Chrome profiles in /tmp/")
            raise

    def _save_session(self):
        """Save cookies for future sessions"""
        try:
            cookies = self.driver.get_cookies()
            with open(self.session_file, 'w') as f:
                json.dump(cookies, f)
            print(f"✓ Session saved to {self.session_file}")
        except Exception as e:
            print(f"Warning: Could not save session: {e}")

    def _load_session(self):
        """Load saved cookies"""
        try:
            with open(self.session_file, 'r') as f:
                cookies = json.load(f)

            # Navigate to the domain first
            self.driver.get("https://runningintheusa.com")
            time.sleep(2)

            # Add cookies
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception:
                    pass  # Some cookies might fail to load

            print(f"✓ Session loaded from {self.session_file}")
        except Exception as e:
            print(f"Note: Could not load saved session: {e}")

    def get_random_delay(self, min_delay: float = 2.0, max_delay: float = 5.0) -> float:
        """Generate a random delay to mimic human behavior"""
        return random.uniform(min_delay, max_delay)

    def wait_for_cloudflare(self, timeout: int = 30):
        """Wait for Cloudflare challenge to complete"""
        print("Waiting for Cloudflare check...")

        start_time = time.time()
        loop_count = 0
        max_loops = 10

        while time.time() - start_time < timeout:
            # Check if we're stuck in a redirect loop
            current_url = self.driver.current_url
            if 'cdn-cgi' in current_url:
                loop_count += 1
                if loop_count > max_loops:
                    print("\n⚠ Cloudflare redirect loop detected!")
                    print("You may need to manually complete the verification.")
                    print("Looking for checkbox or CAPTCHA in the browser window...")
                    return False
            else:
                loop_count = 0  # Reset if we're on a normal page

            # Check for common Cloudflare elements
            page_source = self.driver.page_source.lower()

            if any(indicator in page_source for indicator in ['cloudflare', 'checking your browser']):
                time.sleep(1)
                continue
            else:
                print("✓ Cloudflare check passed")
                return True

        print("⚠ Cloudflare verification timeout")
        return False

    def scrape_page(self, url: str, is_first_page: bool = False) -> List[Dict[str, str]]:
        """
        Scrape a single page for race information

        Args:
            url: The URL to scrape
            is_first_page: Whether this is the first page (for manual verification)

        Returns:
            List of dictionaries containing race information
        """
        try:
            # Add human-like delay
            time.sleep(self.get_random_delay())

            print(f"Loading page: {url}")
            self.driver.get(url)

            # Wait for Cloudflare on first page
            if is_first_page:
                print("\n" + "=" * 70)
                print("IMPORTANT: A Chrome browser window should be visible.")
                print("Keep it visible - you may need to complete a verification.")
                print("=" * 70)

                self.wait_for_cloudflare(timeout=30)

                # Manual verification step
                print("\n" + "=" * 70)
                print("MANUAL VERIFICATION")
                print("=" * 70)
                print("\nIf you see a verification challenge:")
                print("  - Complete any CAPTCHA")
                print("  - Click verification checkboxes")
                print("  - Wait for the page to load completely")
                print("\nOnce you see race listings, verification is complete.")
                print("=" * 70)

                input("\nPress ENTER when you can see race listings...")

                # Save the session for future use
                self._save_session()

                print("\n✓ Verification completed! Continuing...\n")

            # Wait for page to load
            time.sleep(self.get_random_delay(3, 5))

            # Scroll to trigger lazy loading
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Get the page source and parse
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            races = []

            # Try multiple possible selectors
            race_items = (
                soup.find_all('div', class_='list-item') or
                soup.find_all('div', class_='race-item') or
                soup.find_all('tr', class_='race') or
                soup.find_all('div', {'data-type': 'race'})
            )

            if not race_items:
                print(f"Warning: No race items found with standard selectors")
                return []

            for item in race_items:
                try:
                    # Extract date
                    date_elem = (
                        item.find('div', class_='date') or
                        item.find('span', class_='date') or
                        item.find('td', class_='date') or
                        item.find(class_=lambda x: x and 'date' in str(x).lower())
                    )

                    if not date_elem:
                        continue

                    date_text = date_elem.get_text(strip=True)

                    # Extract race name
                    name_elem = (
                        item.find('a', class_='thick') or
                        item.find('a', class_='race-name') or
                        item.find('h3') or
                        item.find('h4') or
                        item.find('a', href=lambda x: x and '/race/' in str(x))
                    )

                    if not name_elem:
                        continue

                    race_name = name_elem.get_text(strip=True)

                    # Extract location
                    location_elem = (
                        item.find('div', class_='location') or
                        item.find('span', class_='location') or
                        item.find('td', class_='location') or
                        item.find(class_=lambda x: x and 'location' in str(x).lower())
                    )

                    if not location_elem:
                        text = item.get_text()
                        import re
                        match = re.search(r'([A-Z]{2})(?:\s|$)', text)
                        if match:
                            location_text = text.split(race_name)[-1].strip()
                        else:
                            continue
                    else:
                        location_text = location_elem.get_text(strip=True)

                    races.append({
                        'Date': date_text,
                        'Race Name': race_name,
                        'Location': location_text
                    })

                except Exception as e:
                    print(f"Error parsing race item: {e}")
                    continue

            return races

        except Exception as e:
            print(f"Error scraping page: {e}")
            return []

    def build_url(self, start_date: str, end_date: str, page: int = 1) -> str:
        """Build the URL for a specific page"""
        base_url = "https://runningintheusa.com/classic/list/map"
        return f"{base_url}/{start_date}-to-{end_date}/10k-to-100m/page-{page}"

    def scrape_date_range(self, start_date: str, end_date: str, max_pages: int = 20) -> List[Dict[str, str]]:
        """
        Scrape all races within a date range

        Args:
            start_date: Start date in MM-DD-YYYY format
            end_date: End date in MM-DD-YYYY format
            max_pages: Maximum number of pages to scrape

        Returns:
            List of all races found
        """
        all_races = []

        print(f"\nStarting scrape for dates: {start_date} to {end_date}")
        print(f"Maximum pages: {max_pages}")
        print("-" * 70)

        for page in range(1, max_pages + 1):
            url = self.build_url(start_date, end_date, page)
            print(f"\nScraping page {page}/{max_pages}...")

            races = self.scrape_page(url, is_first_page=(page == 1))

            if not races:
                print(f"No races found on page {page}. Stopping pagination.")
                break

            all_races.extend(races)
            print(f"✓ Found {len(races)} races on page {page}")
            print(f"Total races so far: {len(all_races)}")

            # If we got fewer races than expected, might be at last page
            if len(races) < 10:
                print("Fewer races than expected. Likely reached the last page.")
                break

        print("-" * 70)
        return all_races

    def export_to_excel(self, races: List[Dict[str, str]], filename: str = None) -> str:
        """Export races to an Excel file"""
        if not races:
            print("No races to export!")
            return None

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"races_{timestamp}.xlsx"

        if not filename.endswith('.xlsx'):
            filename += '.xlsx'

        df = pd.DataFrame(races)
        df.to_excel(filename, index=False, engine='openpyxl')

        print(f"\n✓ Successfully exported {len(races)} races to {filename}")
        return filename

    def close(self):
        """Close the browser"""
        if hasattr(self, 'driver'):
            self.driver.quit()
            print("✓ Browser closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def main():
    """Main function to run the advanced scraper"""
    print("\n" + "=" * 70)
    print("Advanced Race Scraper - Cloudflare Loop Workaround")
    print("=" * 70)
    print("\nThis scraper uses advanced techniques to bypass Cloudflare:")
    print("✓ Undetected ChromeDriver (invisible to bot detection)")
    print("✓ Session persistence (saves cookies for future runs)")
    print("✓ Loop detection (prevents getting stuck)")
    print("✓ Human-like behavior (scrolling, delays)")
    print("=" * 70)

    # Get user input
    print("\nEnter date range in MM-DD-YYYY format")
    start_date = input("Start date (e.g., 01-31-2026): ").strip()
    end_date = input("End date (e.g., 02-01-2026): ").strip()

    # Validate date format
    try:
        datetime.strptime(start_date, "%m-%d-%Y")
        datetime.strptime(end_date, "%m-%d-%Y")
    except ValueError:
        print("Error: Invalid date format. Please use MM-DD-YYYY format.")
        sys.exit(1)

    # Ask for max pages
    max_pages_input = input("Maximum pages to scrape (default 20): ").strip()
    max_pages = int(max_pages_input) if max_pages_input else 20

    # Ask for output filename
    output_file = input("Output filename (press Enter for auto-generated): ").strip()
    if not output_file:
        output_file = None

    print("\n" + "=" * 70)
    print("IMPORTANT: A Chrome browser window will open.")
    print("Keep it visible - you may need to complete a verification challenge.")
    print("=" * 70)

    # Run scraper
    try:
        with AdvancedRaceScraper(headless=False, use_saved_session=True) as scraper:
            races = scraper.scrape_date_range(start_date, end_date, max_pages)

            if races:
                # Export to Excel
                filename = scraper.export_to_excel(races, output_file)

                # Display summary
                print("\n" + "=" * 70)
                print("SUMMARY")
                print("=" * 70)
                print(f"Total races found: {len(races)}")
                print(f"Output file: {filename}")
                print("\nSample of first 3 races:")
                for i, race in enumerate(races[:3], 1):
                    print(f"{i}. {race['Date']}, {race['Race Name']}, {race['Location']}")
                print("=" * 70)
            else:
                print("\nNo races found for the specified date range.")

    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
