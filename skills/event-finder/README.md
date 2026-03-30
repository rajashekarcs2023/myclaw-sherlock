# Event Finder Skill

A skill for finding real-time events (hackathons, meetups, conferences) with **automatic date validation and time-sensitive query handling**.

## Features

✅ **Automatic time validation** — always checks current date/time before searching
✅ **Live data fetching** — pulls fresh data from Eventbrite, Meetup, Devpost, Luma
✅ **Date filtering** — filters results to match user's time window
✅ **Platform coverage** — Major event platforms out-of-the-box

## Installation

This skill is already installed in your workspace at:
```
~/.openclaw/workspace/skills/event-finder/
```

## Usage

Simply ask the agent about events with time queries:

```
"hackathons this weekend in San Francisco"
"AI meetups tomorrow"
"conferences next week in New York"
"workshops today near me"
```

The skill will:

1. Check the current date/time via `session_status`
2. Parse your time phrase into a date range
3. Fetch live events from Eventbrite (and other platforms)
4. Filter results to match your time window
5. Return formatted output with date validation

## File Structure

```
event-finder/
├── SKILL.md                    # Complete documentation and usage guide
├── references/
│   ├── PLATFORMS.md           # Platform URLs and city patterns
│   └── TESTING.md             # Test cases and expected outputs
└── scripts/
    ├── parse_dates.py         # Date parsing utilities
    ├── eventbrite_url.py      # Generate Eventbrite search URLs
    └── test_parser.py         # Test date parsing logic
```

## How It Works

See [SKILL.md](./SKILL.md) for complete implementation guide:

- **Time validation rules** — how to check and validate dates
- **Platform fetching** — how to pull data from each platform
- **Date parsing** — converting "this weekend" to actual date ranges
- **Filtering logic** — ensuring results match user's time window
- **Output formatting** — clean, scannable event listings

## Test the Scripts

Test the date parsing logic:

```bash
cd ~/.openclaw/workspace/skills/event-finder/scripts
python3 test_parser.py
```

Generate Eventbrite URLs:

```bash
python3 eventbrite_url.py "San Francisco" CA "hackathon"
python3 eventbrite_url.py "New York" NY "meetup"
```

## Why This Matters

Without time validation, agents often return:
- Search results from cached snippets (January 2025 events when asking "this weekend" in March 2026)
- Outdated listings that expired months ago
- Incorrect relative date parsing

This skill fixes that by:
- Proactively checking current date/time
- Fetching live data (not cached search results)
- Validating all returned dates against the expected range
- Explicitly stating the date range used for each query

## License

Part of OpenClaw workspace configuration.
