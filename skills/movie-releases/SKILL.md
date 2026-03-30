---
name: movie-releases
description: Get the latest movie releases, ratings, and reviews from TMDB. AUTOMATICALLY SENDS RESULTS TO EMAIL when requested. Perfect for queries like "send me top 10 movies to john@example.com".
author: Sherlock
version: 1.0.0
---

# Movie Releases Skill 🎬

Search for the latest movie releases, ratings, reviews, and detailed information from TMDB (The Movie Database).

## What This Skill Does

- **Latest Releases:** Find new movies released in theaters or on streaming platforms
- **Movie Ratings:** Get critic and audience scores, vote counts, and popularity metrics
- **Detailed Info:** Cast, director, runtime, genres, plot summaries, and release dates
- **Search:** Look up specific movies by title or keywords
- **Top Rated:** Discover highly-rated films
- **Now Playing:** See what's currently in theaters

## When to Use This Skill

Use when a user asks about:
- Latest movie releases this month/week
- New Hollywood movies
- Movie ratings and reviews
- Current movies in theaters
- Top-rated films
- Information about a specific movie
- Cast, director, or runtime details

Examples:
- "What are the latest movie releases this month in Hollywood?"
- "What are the top-rated movies right now?"
- "What's playing in theaters near me?"
- "What's the rating for [movie name]?"
- "Who stars in the new [movie title]?"

## How It Works

This skill uses the **TMDB API** (The Movie Database) to fetch movie data:
- Free tier available at https://www.themoviedb.org/settings/api
- No API key required for basic usage (demo key included)
- Set `TMDB_API_KEY` environment variable or create `~/.openclaw/.tmdb_creds.json` with your key

## Usage

### For AI Agents

When a movie-related query is detected:

1. **Identify the query type:**
   - Latest releases → use `latest` command
   - Search specific movie → use `search` command
   - Top-rated → use `top-rated` command
   - Now playing → use `now-playing` command

2. **Extract parameters:**
   - Region: Country code (default: "US", "GB", "IN", etc.)
   - Timeframe: Days back for latest (default: 30)
   - Query: Movie title or keywords
   - Limit: Maximum results (default: 10)

3. **Execute the script:**
   ```bash
   cd ~/.openclaw/workspace/skills/public/movie-search
   python3 scripts/movie_search.py <command> [args]
   ```

4. **Format and present results** to the user

### Commands

```bash
# Latest releases (default: last 30 days in US)
python3 scripts/movie_search.py latest [region] [days]

# Search for a movie
python3 scripts/movie_search.py search "Dune" [year]

# Top-rated movies
python3 scripts/movie_search.py top-rated [region]

# Now playing in theaters
python3 scripts/movie_search.py now-playing [region]
```

### Examples

```bash
# Latest Hollywood releases (US, last 30 days)
python3 scripts/movie_search.py latest US 30

# Latest UK releases (last 14 days)
python3 scripts/movie_search.py latest GB 14

# Search for "Dune" (any year)
python3 scripts/movie_search.py search "Dune"

# Search for "Dune" from 2024
python3 scripts/movie_search.py search "Dune" 2024

# Top-rated movies in India
python3 scripts/movie_search.py top-rated IN

# What's playing in theaters now (US)
python3 scripts/movie_search.py now-playing US
```

## Output Format

The script returns structured movie data with:
- Title and release year
- Rating (0-10 scale) and vote count
- Runtime
- Genres
- Top 3 cast members
- Director
- Plot summary (truncated)

Example:
```
1. **Dune: Part Two** (2024)
   ⭐ Rating: 8.4/10 (12,345 votes)
   ⏱️  Runtime: 2h 46m
   🎭 Genres: Science Fiction, Adventure, Action
   🎬 Cast: Timothée Chalamet, Zendaya, Austin Butler
   🎥 Director: Denis Villeneuve
   📝 Paul Atreides unites with Chani and the Fremen while on a warpath of revenge...
```

## Setup

### Prerequisites

Install Python dependencies:
```bash
pip3 install requests
```

### API Key (Optional)

**Demo key included** - Works for testing but has usage limits.

To get your own free API key:
1. Go to https://www.themoviedb.org/settings/api
2. Create an account (free)
3. Generate an API key
4. Set environment variable:
   ```bash
   export TMDB_API_KEY="your-key-here"
   ```
   Or create credential file:
   ```bash
   mkdir -p ~/.openclaw
   echo '{"api_key": "your-key-here"}' > ~/.openclaw/.tmdb_creds.json
   ```

## Integration with Email

To send movie results via email, combine with email functionality:

```bash
# Get latest releases and save to file
python3 scripts/movie_search.py latest US 30 > /tmp/movies.txt

# Send via email (assuming email helper exists)
node ~/.openclaw/workspace/helpers/send-email-cli.mjs \
  "recipient@example.com" \
  "Latest Movie Releases" \
  "$(cat /tmp/movies.txt)"
```

## Agent Implementation Notes

**Query Detection Patterns:**
- "latest [movies/films/releases]" → `latest` command
- "new [Hollywood/Bollywood] movies" → `latest` command with region
- "what's playing" or "in theaters" → `now-playing` command
- "top rated" or "best movies" → `top-rated` command
- "rated" or "rating for [movie]" → `search` command
- "[Movie name]" or "tell me about [movie]" → `search` command

**Region Mapping:**
- US/United States/USA/Hollywood → "US"
- GB/United Kingdom/UK → "GB"
- IN/India/Bollywood → "IN"
- FR/France → "FR"
- DE/Germany → "DE"
- (Add more as needed)

**Timeframe Extraction:**
- "this month" → 30 days
- "this week" → 7 days
- "past 2 weeks" → 14 days
- "last 3 months" → 90 days

## Resources

- **TMDB API:** https://www.themoviedb.org/documentation/api
- **Script:** `scripts/movie_search.py`
- **Demo API Key:** Included (limited usage)

## Notes

- Demo key has rate limits; get your own key for production use
- Release dates vary by region (theatrical vs digital)
- Ratings are based on TMDB user votes (not critic scores)
- Some movies may not have all details available
