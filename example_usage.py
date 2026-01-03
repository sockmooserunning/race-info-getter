#!/usr/bin/env python3
"""
Example usage of the Race Scraper
This demonstrates how to use the scraper programmatically
"""

from race_scraper import RaceScraper


def example_basic_usage():
    """Basic example: scrape races and export to Excel"""
    print("Example 1: Basic Usage")
    print("-" * 60)

    # Create scraper instance
    scraper = RaceScraper()

    # Scrape races for a specific date range
    races = scraper.scrape_date_range(
        start_date="01-31-2026",
        end_date="02-01-2026",
        max_pages=3  # Limit to 3 pages for this example
    )

    # Export to Excel with custom filename
    if races:
        scraper.export_to_excel(races, "example_races.xlsx")

        # Print first few races
        print("\nFirst 5 races:")
        for i, race in enumerate(races[:5], 1):
            print(f"{i}. {race['Date']}, {race['Race Name']}, {race['Location']}")
    else:
        print("No races found!")


def example_custom_processing():
    """Example: scrape and do custom processing"""
    print("\n\nExample 2: Custom Processing")
    print("-" * 60)

    scraper = RaceScraper()

    # Scrape races
    races = scraper.scrape_date_range(
        start_date="01-31-2026",
        end_date="02-01-2026",
        max_pages=2
    )

    if races:
        # Custom processing: filter races by state
        target_state = "UT"
        utah_races = [r for r in races if r['Location'].endswith(target_state)]

        print(f"\nFound {len(utah_races)} races in {target_state}:")
        for race in utah_races:
            print(f"  - {race['Race Name']} on {race['Date']}")

        # You could also:
        # - Group by state
        # - Filter by date
        # - Sort by location
        # - Export filtered results


def example_multiple_date_ranges():
    """Example: scrape multiple date ranges"""
    print("\n\nExample 3: Multiple Date Ranges")
    print("-" * 60)

    scraper = RaceScraper()
    all_races = []

    # List of date ranges to scrape
    date_ranges = [
        ("01-01-2026", "01-15-2026"),
        ("02-01-2026", "02-15-2026"),
        ("03-01-2026", "03-15-2026"),
    ]

    for start, end in date_ranges:
        print(f"\nScraping {start} to {end}...")
        races = scraper.scrape_date_range(start, end, max_pages=5)
        all_races.extend(races)

    print(f"\nTotal races from all date ranges: {len(all_races)}")

    # Export all races to one file
    if all_races:
        scraper.export_to_excel(all_races, "multiple_ranges.xlsx")


if __name__ == "__main__":
    # Run examples
    # Uncomment the example you want to run

    example_basic_usage()
    # example_custom_processing()
    # example_multiple_date_ranges()
