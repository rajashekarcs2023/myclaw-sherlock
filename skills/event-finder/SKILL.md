# Event Finder Skill

**Purpose:** Find real-time events (hackathons, meetups, conferences, etc.) with proper date validation and time-sensitive query handling.

## When to Use This Skill

Use when the user asks about:
- Hackathons, meetups, conferences, workshops
- Events with time constraints: "this weekend", "tomorrow", "next week", "today"
- Venue-based events: "in San Francisco", "in New York", etc.
- Specific platforms: Eventbrite, Meetup, Devpost, Luma events

## Key Features

1. **Automatic Time Validation:** Always checks current date/time before searching
2. **Live Data Fetching:** Pulls fresh data from event platforms (not cached search snippets)
3. **Date Filtering:** Filters results to match user's time window
4. **Platform Coverage:** Eventbrite, Meetup, Devpost, Luma

## How to Use

### Basic Query Syntax

```
"hackathons this weekend in San Francisco"
"AI meetups tomorrow"
"conferences next week in New York"
"workshops today near me"
```

### Supported Platforms

- Eventbrite (primary - most comprehensive)
- Meetup (meetup.com)
- Devpost (hackathons only)
- Luma (tech/early-stage events)

### Supported Time Queries

- "today", "tomorrow", "yesterday"
- "this weekend", "next weekend", "last weekend"
- "this week", "next week", "last week"
- "in 3 days", "within 2 weeks"
- Specific dates: "March 30 2026", "next Tuesday"

## Implementation Guide

### Step 1: Get Current Date/Time

ALWAYS call `session_status` first to get current date/time. Extract:
- Current date
- Day of week (Sunday-Saturday)
- Timezone (assume America/Los_Angeles unless user specifies otherwise)

### Step 2: Parse Time Query

Convert user's time phrase into a date range:

| User Query | Date Range |
|------------|-------------|
| "today" | Current date only |
| "tomorrow" | Current date + 1 day |
| "yesterday" | Current date - 1 day |
| "this weekend" | Friday-Sunday of current week (if today is Friday, count today through Sunday; if Saturday, today-Sunday; if Sunday, today only) |
| "next weekend" | Friday-Sunday of next week |
| "this week" | Monday-Sunday of current week |
| "next week" | Monday-Sunday of next week |
| "in N days" | Today to Today + N days |
| "within N weeks" | Today to Today + (N × 7) days |

### Step 3: Fetch Events by Platform

#### Eventbrite (Primary)

**Fetch URL Pattern:**
```
https://www.eventbrite.com/d/{state-short}--{city}/{category}--events/
```

**Examples:**
- San Francisco hackathons: `https://www.eventbrite.com/d/ca--san-francisco/hackathon--events/`
- New York meetups: `https://www.eventbrite.com/d/ny--new-york/meetup--events/`
- Austin conferences: `https://www.eventbrite.com/d/tx--austin/conference--events/`

**Categories to use:**
- hackathon
- meetup
- conference
- workshop
- seminar
- networking
- (or no category for all events)

**Fetch with web_fetch tool:**
```json
{
  "url": "https://www.eventbrite.com/d/ca--san-francisco/hackathon--events/",
  "extractMode": "markdown",
  "maxChars": 15000
}
```

#### Meetup.com

**Search URL Pattern:**
```
https://www.meetup.com/find/{location}/?keywords={query}
```

**Example:**
```
https://www.meetup.com/find/san-francisco/?keywords=hackathon
```

**Note:** Meetup may require JavaScript. If web_fetch returns minimal content, use web_search with site:meetup.com filter.

#### Devpost (Hackathons Only)

**Base URL:**
```
https://devpost.com/hackathons
```

**Search query:**
```
https://devpost.com/hackathons?q={query}&sort=Deadline+Ascending
```

**Note:** Devpost often requires JS rendering. Use web_search with site:devpost.com as fallback.

#### Luma (Tech Events)

**Search URL Pattern:**
```
https://lu.ma/search?q={query}
```

**Example:**
```
https://lu.ma/search?q=san+francisco+hackathon
```

### Step 4: Parse and Filter Events

From fetched content, extract:

- Event name/title
- Date/time (parse relative dates like "Today at 9:00 AM", "Sat, Jun 27")
- Location (city, venue address)
- Registration URL
- Price if displayed

**Then filter by date range:**

1. Convert all dates to absolute dates (use current date as anchor)
2. Include events that fall within user's requested date range
3. Explicitly exclude events clearly outside range (e.g., January event when asking "this weekend" in March)
4. Flag borderline cases with note: "Ends slightly outside requested window"

### Step 5: Format Output

Present results in a clean, scannable format:

```markdown
## [Date Category]

### Event Title
- **When:** Date & time
- **Location:** Venue address, City
- [Registration Link](url)
- Brief description if available
- Price if specified
```

**Add validation section at bottom:**
```markdown
---
**Time Validation:**
- Current date/time: [day], [date], [time] [timezone]
- Your query: "[user's time phrase]" → [calculated date range]
- All events above fall within this window ✓
```

## Date Parsing Reference

### Relative Date Keywords to Absolute

| Keyword | Conversion Logic |
|---------|-----------------|
| "Today" | Current date |
| "Tomorrow" | Current date + 1 day |
| "yesterday" | Current date - 1 day |
| "This [dayname]" | Next occurrence of day (including today if matches) |
| "Next [dayname]" | _After_ the next occurrence (skip this week's) |
| "This weekend" | Friday, Saturday, Sunday of current week |
| "This week" | Monday through Sunday of current week |
| "Next weekend" | Friday, Saturday, Sunday of next week |
| "Next week" | Monday through Sunday of next week |
| "in N days" | Today + N days |
| "within N days" | Today through Today + N days |
| "within N weeks" | Today through Today + (N × 7) days |

### Day of Week Calculation

If current date is Saturday, March 28, 2026:

| Query | Result |
|-------|--------|
| "this Monday" | March 24 (earlier in current week, so "this Monday" means next Monday: March 31) |
| "this Tuesday" | March 25 (earlier, so next Tuesday: April 1) |
| "this Friday" | Already passed Friday (March 27), so next Friday: April 3 |
| "this Saturday" | Today, March 28 |
| "this Sunday" | March 29 |
| "next Saturday" | April 4 |

**Special case:** If user says "this weekend" on Friday, include Friday-Sunday. If Saturday, include Saturday-Sunday. If Sunday, include today only.

## Fallback Behavior

If live fetching fails or returns no results:

1. Try alternative platforms (e.g., if Eventbrite fails, try Meetup)
2. Use web_search with date-specific query:
   ```
   "hackathons San Francisco March 29 2026 OR March 30 2026"
   ```
3. Be honest about limitations:
   ```
   "I couldn't fetch live events from Eventbrite. Here are search results which may include outdated listings. Please verify dates before registering."
   ```

## Common Mistakes to Avoid

❌ **Don't trust cached search snippets:** Always validate dates against current time.

❌ **Don't infer relative dates from old results:** A result showing "Saturday, Jan 25" from 2025 is NOT this Saturday.

❌ **Don't ignore timezone:** Convert times to user's timezone when displaying.

❌ **Don't skip session_status:** Always call it first, even if you "think" you know the date.

✅ **Do:** Explicitly state the date range you're using.

✅ **Do:** Flag results that seem outdated or questionable.

✅ **Do:** Provide direct links for registration so user can verify.

## Example Workflow

**User asks:** "hackathons this weekend in San Francisco"

1. Call `session_status` →得知 Saturday, March 28, 2026, America/Los_Angeles
2. Parse "this weekend" → March 28 (today) through March 29 (Sunday)
3. Fetch Eventbrite: `https://www.eventbrite.com/d/ca--san-francisco/hackathon--events/`
4. Parse events, filter for March 28-29, 2026
5. Return:
   - Events matching date range
   - Time validation note showing current date and calculated range
   - Clear formatting with registration links

## Testing

To test this skill, try queries like:

- "hackathons this weekend in San Francisco" (should return today + tomorrow)
- "meetups tomorrow" (should return only next day's events)
- "conferences next week" (should return events 7-14 days out)
- "events today near me" (should return today's events only)

Verify that:
- Dates match current calendar
- No outdated results from previous months/years
- Relative date words convert correctly
- Validation section appears at bottom

## References

- Eventbrite search API docs: https://www.eventbrite.com/platform/api/
- Meetup search: https://www.meetup.com/find/
- Devpost hackathons: https://devpost.com/hackathons
- OpenClaw web_fetch tool docs
