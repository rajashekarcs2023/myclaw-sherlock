# Test Case: Weekend Hackathon Query

**User Query:** "hackathons this weekend in San Francisco"

**Expected Behavior:**
1. Call session_status → get Saturday, March 28, 2026
2. Parse "this weekend" → March 28 (today) + March 29 (Sunday)
3. Fetch Eventbrite San Francisco hackathons
4. Filter for March 28-29 only
5. Return 2 events with date validation

**Expected Output Format:**
```markdown
## This Weekend (Saturday)

### MeetStream AI x Scalekit Hackathon — Build Day SF
- **When:** Today (Saturday, March 28) at 9:00 AM
- **Location:** 144 Townsend St, San Francisco
- [Register](...)
- Focus: AI/Scalekit building day — a free hackathon

## This Weekend (Sunday)

### [Any Sunday hackathons with details]

---
**Time Validation:**
- Current date/time: Saturday, March 28, 2026, 14:15 PDT
- Your query: "this weekend" → March 28-29, 2026 (Saturday-Sunday)
- All events above fall within this window ✓
```

---

# Test Case: Tomorrow Query

**User Query:** "meetups tomorrow"

**Expected:** Only events on March 29, 2026 (Sunday)

---

# Test Case: Specific Date Query

**User Query:** "conferences on April 5, 2026 in San Francisco"

**Expected:** Only events on exactly April 5, 2026

---

# Test Case: Outdated Result Detection

**Scenario:** Search returns event from January 2025

**Expected Behavior:**
- Detect date mismatch (Jan 2025 vs March 2026 current)
- Exclude from results or flag as outdated
- Add note: "Search returned outdated results for January 2025, excluded from above list"
