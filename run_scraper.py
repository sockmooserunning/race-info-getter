#!/usr/bin/env python3
"""
Interactive launcher for race scrapers
Helps users choose and run the appropriate scraper
"""

import sys
import os


def main():
    print("=" * 70)
    print("                    RACE INFO SCRAPER")
    print("              runningintheusa.com Data Extractor")
    print("=" * 70)
    print()
    print("Choose your scraping method:")
    print()
    print("1. Selenium Scraper (RECOMMENDED)")
    print("   ✓ Uses real Chrome browser with manual verification")
    print("   ✓ You complete the human verification step")
    print("   ✓ Then scraping continues automatically")
    print("   ✓ Most reliable method")
    print("   ✗ Requires Chrome browser installed")
    print()
    print("2. Requests Scraper (Lightweight - NOT RECOMMENDED)")
    print("   ✓ Fast and lightweight")
    print("   ✓ No browser required")
    print("   ✗ Usually blocked by website bot detection")
    print("   ✗ Will likely fail to collect data")
    print()

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        print("\nLaunching Selenium Scraper...")
        print("-" * 70)
        print()
        # Check if file exists
        if not os.path.exists("race_scraper_selenium.py"):
            print("Error: race_scraper_selenium.py not found!")
            sys.exit(1)

        # Import and run
        try:
            from race_scraper_selenium import main as selenium_main
            selenium_main()
        except ImportError as e:
            print(f"\nError: Missing dependencies!")
            print(f"Please run: pip install -r requirements.txt")
            print(f"\nDetails: {e}")
            sys.exit(1)

    elif choice == "2":
        print("\nLaunching Requests Scraper...")
        print("-" * 70)
        print()
        # Check if file exists
        if not os.path.exists("race_scraper.py"):
            print("Error: race_scraper.py not found!")
            sys.exit(1)

        # Import and run
        try:
            from race_scraper import main as requests_main
            requests_main()
        except ImportError as e:
            print(f"\nError: Missing dependencies!")
            print(f"Please run: pip install -r requirements.txt")
            print(f"\nDetails: {e}")
            sys.exit(1)

    else:
        print("\nInvalid choice. Please run again and enter 1 or 2.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCancelled by user.")
        sys.exit(0)
