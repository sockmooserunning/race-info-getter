#!/usr/bin/env python3
"""Quick test of the race scraper"""

from race_scraper import RaceScraper

# Test with the example date range provided by the user
scraper = RaceScraper()

print("Testing scraper with 01-31-2026 to 02-01-2026...")
print("Scraping only 2 pages for testing...\n")

races = scraper.scrape_date_range(
    start_date="01-31-2026",
    end_date="02-01-2026",
    max_pages=2  # Just test 2 pages
)

if races:
    print(f"\n✓ Successfully scraped {len(races)} races!")
    print("\nFirst 5 races in the format you requested:")
    print("(Date, Name, Location)")
    print("-" * 60)
    for race in races[:5]:
        print(f"{race['Date']}, {race['Race Name']}, {race['Location']}")

    # Export to test file
    scraper.export_to_excel(races, "test_output.xlsx")
else:
    print("❌ No races found. There might be an issue with the scraper.")
