# Movie Search Skill Installation

## Quick Setup

1. **Install Python dependencies:**
   ```bash
   pip3 install -r scripts/requirements.txt
   ```

2. **Test the skill:**
   ```bash
   cd ~/.openclaw/workspace/skills/public/movie-search
   python3 scripts/movie_search.py latest US 7
   ```

3. **Optional - Get your own TMDB API key:**
   - Visit: https://www.themoviedb.org/settings/api
   - Create account (free)
   - Generate API key
   - Set environment variable:
     ```bash
     export TMDB_API_KEY="your-key-here"
     ```
   - Or save to file:
     ```bash
     mkdir -p ~/.openclaw
     echo '{"api_key": "your-key-here"}' > ~/.openclaw/.tmdb_creds.json
     ```

## What You Can Do

```bash
# Latest releases (Hollywood/US, last 30 days)
python3 scripts/movie_search.py latest US 30

# Search for a specific movie
python3 scripts/movie_search.py search "Dune: Part Two"

# Top-rated movies
python3 scripts/movie_search.py top-rated US

# What's in theaters now
python3 scripts/movie_search.py now-playing US
```

## Email Integration

```bash
# Get movie info and email it
python3 scripts/movie_search.py latest US 30 > /tmp/movies.txt
node ~/.openclaw/workspace/helpers/send-email-cli.mjs \
  "your-email@example.com" \
  "Latest Movies" \
  "$(cat /tmp/movies.txt)"
```

## Notes

- Demo API key included for testing (rate limited)
- Movie data from TMDB (TheMovieDB.org)
- Free and open source
