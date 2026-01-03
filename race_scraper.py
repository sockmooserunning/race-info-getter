#!/usr/bin/env python3
"""
Race Scraper for runningintheusa.com
Extracts race information (date, name, location) and exports to Excel
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
from datetime import datetime
from typing import List, Dict
import sys
import urllib3

try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False

# Disable SSL warnings (for environments with SSL issues)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RaceScraper:
    """Scrapes race information from runningintheusa.com"""

    def __init__(self, use_cloudscraper: bool = True):
        """
        Initialize the scraper

        Args:
            use_cloudscraper: Use cloudscraper to bypass bot protection (default: True)
        """
        # Rotate user agents to appear more human-like
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        ]

        # Use cloudscraper if available and requested
        if use_cloudscraper and CLOUDSCRAPER_AVAILABLE:
            print("Using cloudscraper to bypass bot protection...")
            self.session = cloudscraper.create_scraper(
                browser={
                    'browser': 'chrome',
                    'platform': 'windows',
                    'mobile': False
                }
            )
        else:
            if use_cloudscraper and not CLOUDSCRAPER_AVAILABLE:
                print("Warning: cloudscraper not available, using regular requests...")
            self.session = requests.Session()

            # Create an adapter with retry logic
            from requests.adapters import HTTPAdapter
            from urllib3.util.retry import Retry

            retry_strategy = Retry(
                total=3,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)

    def get_random_delay(self, min_delay: float = 2.0, max_delay: float = 5.0) -> float:
        """Generate a random delay to mimic human behavior"""
        return random.uniform(min_delay, max_delay)

    def get_headers(self, referer: str = None) -> Dict[str, str]:
        """Get random headers to appear more human-like"""
        headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
        }
        if referer:
            headers['Referer'] = referer
        return headers

    def scrape_page(self, url: str) -> List[Dict[str, str]]:
        """
        Scrape a single page for race information

        Args:
            url: The URL to scrape

        Returns:
            List of dictionaries containing race information
        """
        try:
            # Add human-like delay before request
            time.sleep(self.get_random_delay())

            # Try with SSL verification first, fallback to no verification if needed
            referer = 'https://runningintheusa.com/' if 'runningintheusa.com' in url else None
            try:
                response = self.session.get(url, headers=self.get_headers(referer), timeout=30, verify=True)
            except requests.exceptions.SSLError:
                print(f"SSL verification failed, trying without verification...")
                response = self.session.get(url, headers=self.get_headers(referer), timeout=30, verify=False)

            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')
            races = []

            # Find all race listings - they are in div elements with class 'list-item'
            race_items = soup.find_all('div', class_='list-item')

            if not race_items:
                print(f"No race items found on page: {url}")
                return []

            for item in race_items:
                try:
                    # Extract date
                    date_elem = item.find('div', class_='date')
                    if not date_elem:
                        continue

                    # The date format is typically "Jan 31, 2026"
                    date_text = date_elem.get_text(strip=True)

                    # Extract race name
                    name_elem = item.find('a', class_='thick')
                    if not name_elem:
                        continue
                    race_name = name_elem.get_text(strip=True)

                    # Extract location (city and state)
                    location_elem = item.find('div', class_='location')
                    if not location_elem:
                        continue
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

        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error scraping page: {e}")
            return []

    def build_url(self, start_date: str, end_date: str, page: int = 1) -> str:
        """
        Build the URL for a specific page

        Args:
            start_date: Start date in MM-DD-YYYY format
            end_date: End date in MM-DD-YYYY format
            page: Page number (default: 1)

        Returns:
            The constructed URL
        """
        base_url = "https://runningintheusa.com/classic/list/map"
        return f"{base_url}/{start_date}-to-{end_date}/10k-to-100m/page-{page}"

    def scrape_date_range(self, start_date: str, end_date: str, max_pages: int = 20) -> List[Dict[str, str]]:
        """
        Scrape all races within a date range

        Args:
            start_date: Start date in MM-DD-YYYY format
            end_date: End date in MM-DD-YYYY format
            max_pages: Maximum number of pages to scrape (default: 20)

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
            print(f"URL: {url}")

            races = self.scrape_page(url)

            if not races:
                print(f"No races found on page {page}. Stopping pagination.")
                break

            all_races.extend(races)
            print(f"Found {len(races)} races on page {page}")
            print(f"Total races so far: {len(all_races)}")
            print("-" * 60)

            # If we got fewer races than expected, we might be at the last page
            if len(races) < 10:  # Assuming typical page has at least 10 races
                print("Fewer races than expected. Likely reached the last page.")
                break

        return all_races

    def export_to_excel(self, races: List[Dict[str, str]], filename: str = None) -> str:
        """
        Export races to an Excel file

        Args:
            races: List of race dictionaries
            filename: Output filename (optional, auto-generated if not provided)

        Returns:
            The filename of the exported file
        """
        if not races:
            print("No races to export!")
            return None

        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"races_{timestamp}.xlsx"

        # Ensure .xlsx extension
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'

        # Create DataFrame and export
        df = pd.DataFrame(races)
        df.to_excel(filename, index=False, engine='openpyxl')

        print(f"\n✓ Successfully exported {len(races)} races to {filename}")
        return filename


def main():
    """Main function to run the scraper"""
    print("=" * 60)
    print("Race Scraper for runningintheusa.com")
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

    # Ask for max pages (default 20)
    max_pages_input = input("Maximum pages to scrape (default 20, press Enter to use default): ").strip()
    max_pages = int(max_pages_input) if max_pages_input else 20

    if max_pages < 1 or max_pages > 50:
        print("Error: Max pages must be between 1 and 50")
        sys.exit(1)

    # Ask for output filename
    output_file = input("Output filename (press Enter for auto-generated): ").strip()
    if not output_file:
        output_file = None

    print()

    # Run scraper
    scraper = RaceScraper()
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


if __name__ == "__main__":
    main()
