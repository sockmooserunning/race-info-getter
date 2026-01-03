#!/usr/bin/env python3
"""
Selenium-based Race Scraper for runningintheusa.com
Uses a real browser to bypass bot protection
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
from typing import List, Dict
import sys


class SeleniumRaceScraper:
    """Scrapes race information using Selenium WebDriver"""

    def __init__(self, headless: bool = False, manual_verification: bool = True):
        """
        Initialize the Selenium scraper

        Args:
            headless: Run browser in headless mode (no GUI) - default False for manual verification
            manual_verification: Pause for manual human verification on first page
        """
        print("Initializing Selenium WebDriver...")

        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless=new')

        # Add arguments to make it less detectable
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        # Exclude the collection of enable-automation switches
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Initialize the driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Execute CDP commands to prevent detection
        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        self.manual_verification = manual_verification
        self.verification_completed = False

        print("✓ WebDriver initialized successfully")

    def get_random_delay(self, min_delay: float = 2.0, max_delay: float = 5.0) -> float:
        """Generate a random delay to mimic human behavior"""
        return random.uniform(min_delay, max_delay)

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

            # Wait for the page to load
            time.sleep(self.get_random_delay(3, 5))

            # Handle manual verification on first page
            if self.manual_verification and not self.verification_completed:
                print("\n" + "=" * 70)
                print("MANUAL VERIFICATION REQUIRED")
                print("=" * 70)
                print("\nA Chrome browser window should have opened.")
                print("Please complete any human verification challenges in the browser:")
                print("  - Click checkboxes")
                print("  - Solve CAPTCHAs")
                print("  - Wait for verification to complete")
                print("\nOnce you see the race listings page, the verification is complete.")
                print("=" * 70)

                input("\nPress ENTER when you have completed the verification and can see race listings...")

                self.verification_completed = True
                print("\n✓ Verification completed! Continuing with automated scraping...\n")

                # Give a moment for any final page loads
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
                print(f"Warning: No race items found with standard selectors")
                print(f"Trying alternative approach...")

                # Try to find links that might be races
                race_links = soup.find_all('a', href=lambda x: x and '/race/' in str(x))
                if race_links:
                    print(f"Found {len(race_links)} potential race links")

                return []

            for item in race_items:
                try:
                    # Extract date - try multiple selectors
                    date_elem = (
                        item.find('div', class_='date') or
                        item.find('span', class_='date') or
                        item.find('td', class_='date') or
                        item.find(class_=lambda x: x and 'date' in str(x).lower())
                    )

                    if not date_elem:
                        continue

                    date_text = date_elem.get_text(strip=True)

                    # Extract race name - try multiple selectors
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

                    # Extract location - try multiple selectors
                    location_elem = (
                        item.find('div', class_='location') or
                        item.find('span', class_='location') or
                        item.find('td', class_='location') or
                        item.find(class_=lambda x: x and 'location' in str(x).lower())
                    )

                    if not location_elem:
                        # Try to extract from text after the race name
                        text = item.get_text()
                        # Look for state abbreviations
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

        print(f"Starting scrape for dates: {start_date} to {end_date}")
        print(f"Maximum pages: {max_pages}")
        print("-" * 60)

        for page in range(1, max_pages + 1):
            url = self.build_url(start_date, end_date, page)
            print(f"Scraping page {page}/{max_pages}...")

            races = self.scrape_page(url)

            if not races:
                print(f"No races found on page {page}. Stopping pagination.")
                break

            all_races.extend(races)
            print(f"Found {len(races)} races on page {page}")
            print(f"Total races so far: {len(all_races)}")
            print("-" * 60)

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
    """Main function to run the Selenium scraper"""
    print("=" * 60)
    print("Selenium Race Scraper for runningintheusa.com")
    print("=" * 60)
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
    print("NOTE: A Chrome browser window will open.")
    print("You will be asked to complete any human verification challenges.")
    print()

    # Run scraper using context manager (non-headless with manual verification by default)
    try:
        with SeleniumRaceScraper(headless=False, manual_verification=True) as scraper:
            races = scraper.scrape_date_range(start_date, end_date, max_pages)

            if races:
                # Export to Excel
                filename = scraper.export_to_excel(races, output_file)

                # Display summary
                print()
                print("=" * 60)
                print("SUMMARY")
                print("=" * 60)
                print(f"Total races found: {len(races)}")
                print(f"Output file: {filename}")
                print()
                print("Sample of first 3 races:")
                for i, race in enumerate(races[:3], 1):
                    print(f"{i}. {race['Date']}, {race['Race Name']}, {race['Location']}")
            else:
                print("\nNo races found for the specified date range.")

    except KeyboardInterrupt:
        print("\n\nScraping interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
