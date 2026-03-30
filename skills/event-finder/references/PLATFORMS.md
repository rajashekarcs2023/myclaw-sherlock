# Event Finder - References

Event platform URLs and patterns for quick reference.

## Platform URLs

### Eventbrite
```
Format: https://www.eventbrite.com/d/{state-short}--{city}/{category}--events/

Categories:
- hackathon
- meetup
- conference
- workshop
- seminar
- networking
- (empty = all events)

Examples:
- SF hackathons: https://www.eventbrite.com/d/ca--san-francisco/hackathon--events/
- NY meetups: https://www.eventbrite.com/d/ny--new-york/meetup--events/
- Austin conferences: https://www.eventbrite.com/d/tx--austin/conference--events/
```

### Meetup.com
```
Format: https://www.meetup.com/find/{city}/?keywords={query}

Example:
- SF hackathons: https://www.meetup.com/find/san-francisco/?keywords=hackathon
```

### Devpost
```
Base: https://devpost.com/hackathons
Search: https://devpost.com/hackathons?q={query}&sort=Deadline+Ascending
```

### Luma
```
Format: https://lu.ma/search?q={query}

Example:
- SF hackathons: https://lu.ma/search?q=san+francisco+hackathon
```

## Common Cities

| City | State | Eventbrite URL |
|------|-------|----------------|
| San Francisco | CA | ca--san-francisco |
| New York | NY | ny--new-york |
| Los Angeles | CA | ca--los-angeles |
| Austin | TX | tx--austin |
| Seattle | WA | wa--seattle |
| Boston | MA | ma--boston |
| Chicago | IL | il--chicago |
| Miami | FL | fl--miami |
| Denver | CO | co--denver |
| Portland | OR | or--portland |

## Time Keywords Reference

| User Query | Date Range Calculation |
|------------|------------------------|
| today | Current date only |
| tomorrow | Current + 1 day |
| yesterday | Current - 1 day |
| this weekend | Fri-Sun of current week (or remaining weekend days if Sat/Sun) |
| next weekend | Fri-Sun of next week |
| this week | Mon-Sun of current week |
| next week | Mon-Sun of next week |
| in N days | Today to Today + N |
| within N days | Today to Today + N |
| within N weeks | Today to Today + (N × 7) |
