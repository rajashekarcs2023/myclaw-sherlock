#!/usr/bin/env python3
"""
Test the parse_dates.py module with example queries.
"""

from parse_dates import parse_relative_date, format_date_range
from datetime import datetime

def test_parser():
    """Test date parsing with various queries."""
    test_date = datetime(2026, 3, 28)  # Saturday, March 28, 2026

    print("=" * 60)
    print(f"Testing with reference date: {test_date.strftime('%A, %B %d, %Y')}")
    print("=" * 60)
    print()

    test_cases = [
        ("today", "Current date only"),
        ("tomorrow", "Next day only"),
        ("yesterday", "Previous day only"),
        ("this weekend", "Friday-Sunday of current week (or remaining weekend)"),
        ("next weekend", "Friday-Sunday of next week"),
        ("this week", "Monday-Sunday of current week"),
        ("next week", "Monday-Sunday of next week"),
        ("in 3 days", "Today + 3 days"),
        ("within 5 days", "Today to today + 5 days"),
        ("within 2 weeks", "Today to today + 14 days"),
    ]

    for query, description in test_cases:
        start, end = parse_relative_date(query, test_date)
        range_str = format_date_range(start, end)

        print(f"Query:   {query:20s}")
        print(f"Meaning: {description}")
        print(f"Range:   {range_str}")
        print()

if __name__ == "__main__":
    test_parser()
