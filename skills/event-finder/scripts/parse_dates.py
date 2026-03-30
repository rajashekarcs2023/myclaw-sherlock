#!/usr/bin/env python3
"""
Event date parser utilities for event-finder skill.

This module provides helper functions for parsing relative date queries
and converting them to absolute date ranges.
"""

from datetime import datetime, timedelta
from typing import Tuple, List

def parse_relative_date(query: str, current_date: datetime) -> Tuple[datetime, datetime]:
    """
    Parse a relative date query and return start/end dates.

    Args:
        query: User's time query (e.g., "today", "this weekend", "next week")
        current_date: Current datetime

    Returns:
        Tuple of (start_date, end_date) as datetime objects
    """
    query = query.lower().strip()

    # Today
    if query == "today":
        return current_date, current_date

    # Tomorrow
    elif query == "tomorrow":
        tomorrow = current_date + timedelta(days=1)
        return tomorrow, tomorrow

    # Yesterday
    elif query == "yesterday":
        yesterday = current_date - timedelta(days=1)
        return yesterday, yesterday

    # This weekend
    elif query == "this weekend":
        return get_weekend_range(current_date)

    # Next weekend
    elif query == "next weekend":
        next_week = current_date + timedelta(weeks=1)
        return get_weekend_range(next_week)

    # This week
    elif query == "this week":
        return get_week_range(current_date, current=True)

    # Next week
    elif query == "next week":
        next_week = current_date + timedelta(weeks=1)
        return get_week_range(next_week, current=False)

    # Parse "in N days" or "within N days"
    elif "in" in query or "within" in query:
        # Simple extraction of number of days
        import re
        match = re.search(r'(\d+)\s*days?', query)
        if match:
            days = int(match.group(1))
            end_date = current_date + timedelta(days=days)
            return current_date, end_date

    # Parse "in N weeks" or "within N weeks"
    elif "week" in query and ("in" in query or "within" in query):
        import re
        match = re.search(r'(\d+)\s*weeks?', query)
        if match:
            weeks = int(match.group(1))
            end_date = current_date + timedelta(weeks=weeks)
            return current_date, end_date

    # Default: return today if unparseable
    return current_date, current_date


def get_weekend_range(date: datetime) -> Tuple[datetime, datetime]:
    """
    Get Friday-Sunday weekend range for a given date.

    Returns:
        Tuple of (start_date, end_date) - Friday to Sunday
    """
    # Day numbering: Monday=0, Tuesday=1, ..., Sunday=6
    days_since_monday = date.weekday()

    # If today is Sunday, just return today
    if days_since_monday == 6:  # Sunday
        return date, date

    # If today is Saturday, return Saturday-Sunday
    if days_since_monday == 5:  # Saturday
        sunday = date + timedelta(days=1)
        return date, sunday

    # For any other day, find Friday of THIS week
    # Friday is weekday 4
    days_to_friday = (4 - days_since_monday)
    friday = date + timedelta(days=days_to_friday)

    # Sunday is 2 days after Friday
    sunday = friday + timedelta(days=2)

    return friday, sunday


def get_week_range(date: datetime, current: bool = True) -> Tuple[datetime, datetime]:
    """
    Get Monday-Sunday week range.

    Args:
        date: Reference date
        current: If True, use this date's week; if False, use next week

    Returns:
        Tuple of (start_date, end_date) - Monday to Sunday
    """
    # Day numbering: Monday=0, ..., Sunday=6
    days_since_monday = date.weekday()
    monday = date - timedelta(days=days_since_monday)
    sunday = monday + timedelta(days=6)

    if not current:
        monday = monday + timedelta(weeks=1)
        sunday = sunday + timedelta(weeks=1)

    return monday, sunday


def format_date_range(start: datetime, end: datetime) -> str:
    """Format a date range for display."""
    if start == end:
        return start.strftime("%B %d, %Y")

    if start.month == end.month:
        if start.day == end.day:
            return start.strftime("%B %d, %Y")
        else:
            return f"{start.strftime('%B %d')} - {end.strftime('%d, %Y')}"

    return f"{start.strftime('%B %d')} - {end.strftime('%B %d, %Y')}"


def is_within_range(event_date: datetime, start: datetime, end: datetime) -> bool:
    """Check if an event date falls within a given range."""
    # Reset time components for date-only comparison
    event_date = event_date.replace(hour=0, minute=0, second=0, microsecond=0)
    start = start.replace(hour=0, minute=0, second=0, microsecond=0)
    end = end.replace(hour=23, minute=59, second=59, microsecond=999999)
    return start <= event_date <= end


if __name__ == "__main__":
    # Test examples
    today = datetime(2026, 3, 28)  # Saturday

    print("Testing with date:", today.strftime("%A, %B %d, %Y"))
    print()

    tests = [
        "today",
        "tomorrow",
        "this weekend",
        "this week",
        "next weekend",
        "next week",
        "in 7 days",
        "within 2 weeks"
    ]

    for query in tests:
        start, end = parse_relative_date(query, today)
        print(f"{query:20s} → {format_date_range(start, end)}")
