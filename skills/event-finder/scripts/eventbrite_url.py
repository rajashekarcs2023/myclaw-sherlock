#!/usr/bin/env python3
"""
Generate Eventbrite search URL for city and category.

Usage:
    python eventbrite_url.py "San Francisco" CA "hackathon"
    python eventbrite_url.py "New York" NY "meetup"
"""

import argparse

def generate_eventbrite_url(city: str, state: str, category: str = "") -> str:
    """
    Generate Eventbrite search URL.

    Args:
        city: City name (e.g., "San Francisco")
        state: State abbreviation (e.g., "CA")
        category: Event category (hackathon, meetup, conference, etc.)

    Returns:
        Eventbrite search URL
    """
    # Format: ca--san-francisco
    location = f"{state.lower()}--{city.lower().replace(' ', '-')}"

    if category:
        return f"https://www.eventbrite.com/d/{location}/{category.lower()}--events/"
    else:
        return f"https://www.eventbrite.com/d/{location}/events/"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Eventbrite search URL")
    parser.add_argument("city", help="City name (e.g., 'San Francisco')")
    parser.add_argument("state", help="State abbreviation (e.g., 'CA')")
    parser.add_argument("category", nargs="?", default="", help="Event category (optional)")

    args = parser.parse_args()

    url = generate_eventbrite_url(args.city, args.state, args.category)
    print(url)
