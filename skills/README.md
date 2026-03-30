# Skills Directory

This directory contains custom skills that extend OpenClaw functionality.

## Available Skills

### event-finder
**Purpose:** Find real-time events (hackathons, meetups, conferences) with automatic date validation.

**Location:** `./event-finder/`

**Use when:** User asks about events with time-sensitive queries ("this weekend", "tomorrow", "next week")

**Files:**
- `SKILL.md` — Complete documentation and implementation guide
- `README.md` — Quick start guide
- `references/PLATFORMS.md` — Platform URLs and city patterns
- `references/TESTING.md` — Test cases and validation examples
- `scripts/parse_dates.py` — Date parsing utilities
- `scripts/eventbrite_url.py` — URL generation utility
- `scripts/test_parser.py` — Parse testing script

**Key Features:**
- ✅ Automatic time validation (calls `session_status` before searching)
- ✅ Live data fetching from Eventbrite, Meetup, Devpost, Luma
- ✅ Date filtering and validation against user's time window
- ✅ Prevents cached/stale results from search snippets

**Example Queries:**
- "hackathons this weekend in San Francisco"
- "AI meetups tomorrow"
- "conferences next week in New York"
- "workshops today near me"

---

## Adding New Skills

To add a new skill, create a directory with:

1. `SKILL.md` — Required. The skill's documentation with `### When to Use This Skill` section
2. `README.md` — Optional. Quick start guide
3. `references/` — Optional. Reference documentation
4. `scripts/` — Optional. Helper scripts and utilities

The SKILL.md file must include:
- `### When to Use This Skill` — Clear trigger conditions
- Implementation details and usage examples
- Any constraints or special behaviors

Skills in this directory are loaded into the workspace context and can be referenced by OpenClaw agents.
