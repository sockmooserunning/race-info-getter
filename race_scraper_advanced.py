#!/usr/bin/env python3
"""
Advanced Race Scraper with Cloudflare Loop Workaround
Uses undetected-chromedriver to reliably bypass Cloudflare protection
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import json
import os
from datetime import datetime
from typing import List, Dict
import sys


class AdvancedRaceScraper:
    """
    Advanced scraper using undetected-chromedriver to bypass Cloudflare
    Includes session persistence and loop detection
    """

    def __init__(self, headless: bool = False, use_saved_session: bool = True):
        """
        Initialize the advanced scraper

        Args:
            headless: Run browser in headless mode (not recommended for first run)
            use_saved_session: Try to use saved cookies from previous successful session
        """
        self.session_file = "cloudflare_session.json"
        self.use_saved_session = use_saved_session
        self.verification_completed = False

        print("=" * 70)
        print("Advanced Race Scraper - Cloudflare Bypass Edition")
        print("=" * 70)
        print("\nInitializing undetected Chrome WebDriver...")
        print("This may take a moment on first run...\n")

        # Configure Chrome options for maximum stealth
        options = uc.ChromeOptions()

        if headless:
            options.add_argument('--headless=new')

        # Stealth arguments
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')

        # Random user agent (will be overridden by undetected-chromedriver)
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # Additional preferences to appear more human
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2,
        }
        options.add_experimental_option("prefs", prefs)

        try:
            # Initialize undetected Chrome (this is the magic!)
            self.driver = uc.Chrome(
                options=options,
                version_main=None,  # Auto-detect Chrome version
                driver_executable_path=None,  # Auto-download driver
                use_subprocess=True,
            )

            print("✓ Undetected ChromeDriver initialized successfully")
            print("✓ Bot detection bypass active\n")

            # Set implicit wait
            self.driver.implicitly_wait(10)

        except Exception as e:
            print(f"✗ Error initializing driver: {e}")
            print("\nTroubleshooting tips:")
            print("1. Make sure Chrome browser is installed")
            print("2. Close all Chrome instances and try again")
            print("3. Delete any existing Chrome profiles in /tmp/")
            raise

    def save_session(self):
        """Save cookies to file for future use"""
        try:
            cookies = self.driver.get_cookies()
            with open(self.session_file, 'w') as f:
                json.dump(cookies, f)
            print(f"✓ Session saved to {self.session_file}")
        except Exception as e:
            print(f"Warning: Could not save session: {e}")

    def load_session(self) -> bool:
        """Load cookies from file"""
        if not os.path.exists(self.session_file):
            return False

        try:
            with open(self.session_file, 'r') as f:
                cookies = json.load(f)

            # Navigate to domain first
            self.driver.get("https://runningintheusa.com")
            time.sleep(2)

            # Add cookies
            for cookie in cookies:
                try:
                    self.driver.add_cookie(cookie)
                except Exception as e:
                    pass  # Some cookies may not be valid

            print("✓ Previous session loaded")
            return True
        except Exception as e:
            print(f"Warning: Could not load session: {e}")
            return False

    def detect_cloudflare_challenge(self) -> bool:
        """Detect if we're stuck in a Cloudflare challenge"""
        try:
            page_source = self.driver.page_source.lower()
            title = self.driver.title.lower()

            # Check for common Cloudflare indicators
            cf_indicators = [
                'checking your browser',
                'cloudflare',
                'just a moment',
                'please wait',
                'verifying you are human',
                'challenge-running',
                'ray id'
            ]

            for indicator in cf_indicators:
                if indicator in page_source or indicator in title:
                    return True

            return False
        except:
            return False

    def wait_for_cloudflare(self, max_wait: int = 30) -> bool:
        """
        Wait for Cloudflare challenge to complete

        Args:
            max_wait: Maximum seconds to wait

        Returns:
            True if challenge passed, False if stuck
        """
        print("⏳ Cloudflare challenge detected, waiting for it to resolve...")

        start_time = time.time()
        last_url = None
        url_change_count = 0

        while time.time() - start_time < max_wait:
            current_url = self.driver.current_url

            # Check if URL is changing (redirect loop)
            if current_url != last_url:
                url_change_count += 1
                last_url = current_url

            # If URL changed more than 5 times, we're likely in a loop
            if url_change_count > 5:
                print("⚠️  Detected redirect loop - Cloudflare may be blocking")
                return False

            # Check if challenge is gone
            if not self.detect_cloudflare_challenge():
                print("✓ Cloudflare challenge passed!")
                return True

            time.sleep(1)
            print(".", end="", flush=True)

        print("\n⚠️  Cloudflare challenge timeout")
        return False

    def get_random_delay(self, min_delay: float = 2.0, max_delay: float = 5.0) -> float:
        """Generate a random delay to mimic human behavior"""
        return random.uniform(min_delay, max_delay)

    def human_like_scroll(self):
        """Perform human-like scrolling"""
        try:
            # Random scroll down
            scroll_amount = random.randint(300, 700)
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 1.5))

            # Maybe scroll back up a bit
            if random.random() > 0.5:
                self.driver.execute_script(f"window.scrollBy(0, -{scroll_amount // 2});")
                time.sleep(random.uniform(0.3, 0.8))
        except:
            pass

    def scrape_page(self, url: str) -> List[Dict[str, str]]:
        """
        Scrape a single page for race information

        Args:
            url: The URL to scrape

        Returns:
            List of dictionaries containing race information
        """
        try:
            # Add human-like delay
            time.sleep(self.get_random_delay())

            print(f"Loading page: {url}")
            self.driver.get(url)

            # Wait a bit for page to load
            time.sleep(self.get_random_delay(2, 4))

            # Check for Cloudflare challenge
            if self.detect_cloudflare_challenge():
                if not self.wait_for_cloudflare(max_wait=30):
                    print("\n" + "=" * 70)
                    print("⚠️  CLOUDFLARE VERIFICATION NEEDED")
                    print("=" * 70)
                    print("\nThe browser window should be visible.")
                    print("Please complete any verification challenge:")
                    print("  - Click 'Verify you are human' checkbox")
                    print("  - Solve any CAPTCHA if presented")
                    print("  - Wait for the page to load completely")
                    print("\nOnce you see the race listings, verification is complete.")
                    print("=" * 70)

                    input("\nPress ENTER when you can see the race listings page...")

                    # Save session after successful manual verification
                    self.save_session()
                    self.verification_completed = True
                    print("✓ Verification completed and session saved!\n")
                else:
                    # Auto-passed, save session
                    if not self.verification_completed:
                        self.save_session()
                        self.verification_completed = True

            # Perform human-like scrolling
            self.human_like_scroll()

            # Wait for content to be visible
            time.sleep(2)

            # Get the page source and parse with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            races = []

            # Try multiple possible selectors for race items
            race_items = (
                soup.find_all('div', class_='list-item') or
                soup.find_all('div', class_='race-item') or
                soup.find_all('tr', class_='race') or
                soup.find_all('div', {'data-type': 'race'})
            )

            if not race_items:
                print(f"⚠️  No race items found on page")
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
                        # Try to find location in text
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
                    print(f"⚠️  Error parsing race item: {e}")
                    continue

            return races

        except Exception as e:
            print(f"✗ Error scraping page: {e}")
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

        # Try to load previous session
        if self.use_saved_session:
            print("\nAttempting to use saved session to bypass Cloudflare...\n")
            if self.load_session():
                self.verification_completed = True

        print(f"Starting scrape for dates: {start_date} to {end_date}")
        print(f"Maximum pages: {max_pages}")
        print("-" * 70)

        for page in range(1, max_pages + 1):
            url = self.build_url(start_date, end_date, page)
            print(f"\nPage {page}/{max_pages}")

            races = self.scrape_page(url)

            if not races:
                print(f"No races found on page {page}. Stopping pagination.")
                break

            all_races.extend(races)
            print(f"✓ Found {len(races)} races on page {page}")
            print(f"Total races so far: {len(all_races)}")

            # If we got fewer races than expected, we might be at the last page
            if len(races) < 10:
                print("Fewer races than expected. Likely reached the last page.")
                break

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
    print()

    # Get user input
    print("Enter date range in MM-DD-YYYY format")
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

    print()
    print("=" * 70)
    print("IMPORTANT: A Chrome browser window will open.")
    print("Keep it visible - you may need to complete a verification challenge.")
    print("=" * 70)
    print()

    # Run scraper using context manager
    try:
        with AdvancedRaceScraper(headless=False, use_saved_session=True) as scraper:
            races = scraper.scrape_date_range(start_date, end_date, max_pages)

            if races:
                # Export to Excel
                filename = scraper.export_to_excel(races, output_file)

                # Display summary
                print()
                print("=" * 70)
                print("SUMMARY")
                print("=" * 70)
                print(f"Total races found: {len(races)}")
                print(f"Output file: {filename}")
                print()
                print("Sample of first 3 races:")
                for i, race in enumerate(races[:3], 1):
                    print(f"{i}. {race['Date']} | {race['Race Name']} | {race['Location']}")
                print()
                print("✓ Session saved for future runs (will be faster next time!)")
            else:
                print("\n⚠️  No races found for the specified date range.")

    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user.")
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
