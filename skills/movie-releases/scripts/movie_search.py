#!/usr/bin/env python3
"""
Movie data search script using TMDB API
Fetches latest releases, ratings, reviews, and detailed movie information
"""

import sys
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Try to import requests, provide helpful error if missing
try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library is required but not installed.", file=sys.stderr)
    print("   Install with: pip3 install requests", file=sys.stderr)
    sys.exit(1)


class MovieSearcher:
    """Search and retrieve movie data from TMDB API"""

    def __init__(self, api_key: Optional[str] = None):
        """Initialize with TMDB API key (from param, env var, or defaults)"""
        self.api_key = api_key or os.environ.get("TMDB_API_KEY")

        # Check if credentials file exists
        if not self.api_key:
            creds_file = os.path.expanduser("~/.openclaw/.tmdb_creds.json")
            try:
                with open(creds_file, 'r') as f:
                    creds = json.load(f)
                    self.api_key = creds.get("api_key")
            except (FileNotFoundError, json.JSONDecodeError):
                pass

        # Fallback to demo key (limited usage) - instruct user to get a free key
        if not self.api_key:
            self.api_key = "2dca580c2a14b55200e784d157207b4d"  # Demo key
            print("⚠️  Using demo TMDB API key (limited usage).", file=sys.stderr)
            print("   Get your free API key at: https://www.themoviedb.org/settings/api", file=sys.stderr)

        if not self.api_key:
            raise ValueError("TMDB API key is required. Set TMDB_API_KEY env var or create ~/.openclaw/.tmdb_creds.json")

        self.base_url = "https://api.themoviedb.org/3"
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: Dict) -> Dict:
        """Make authenticated request to TMDB API"""
        params.update({"api_key": self.api_key})
        response = self.session.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    def get_latest_releases(
        self,
        region: str = "US",
        days_back: int = 30,
        media_type: str = "movie"
    ) -> List[Dict]:
        """
        Get latest movie releases in a region

        Args:
            region: Country code (e.g., "US", "GB", "IN")
            days_back: How many days back to search
            media_type: "movie" or "tv"

        Returns:
            List of movie/TV items with details
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        params = {
            "with_release_type": "2|3",  # Theatrical or Digital releases
            "region": region,
            "release_date.gte": start_date.strftime("%Y-%m-%d"),
            "release_date.lte": end_date.strftime("%Y-%m-%d"),
            "sort_by": "popularity.desc"
        }

        try:
            data = self._make_request("discover/movie", params)
            movies = data.get("results", [])

            # Enrich with ratings
            for movie in movies:
                movie["full_details"] = self.get_movie_details(movie["id"])

            return movies
        except Exception as e:
            print(f"❌ Error fetching latest releases: {e}", file=sys.stderr)
            return []

    def search_movies(
        self,
        query: str,
        year: Optional[int] = None,
        limit: int = 10
    ) -> List[Dict]:
        """
        Search for movies by title

        Args:
            query: Movie title or keyword
            year: Optional year filter
            limit: Maximum results to return

        Returns:
            List of matching movies with details
        """
        params = {
            "query": query,
            "page": 1
        }

        if year:
            params["year"] = year

        try:
            data = self._make_request("search/movie", params)
            results = data.get("results", [])[:limit]

            # Enrich with full details
            for movie in results:
                movie["full_details"] = self.get_movie_details(movie["id"])

            return results
        except Exception as e:
            print(f"❌ Error searching movies: {e}", file=sys.stderr)
            return []

    def get_movie_details(self, movie_id: int) -> Dict:
        """
        Get complete details for a movie including ratings, reviews, etc.

        Args:
            movie_id: TMDB movie ID

        Returns:
            Complete movie details
        """
        try:
            # Basic details + credits + similar
            details = self._make_request(f"movie/{movie_id}", {
                "append_to_response": "credits,similar,reviews"
            })
            return details
        except Exception as e:
            print(f"❌ Error fetching movie details: {e}", file=sys.stderr)
            return {}

    def get_top_rated(self, region: str = "US", limit: int = 10) -> List[Dict]:
        """
        Get top-rated movies

        Args:
            region: Country code
            limit: Maximum results

        Returns:
            List of top-rated movies
        """
        try:
            params = {"region": region}
            data = self._make_request("movie/top_rated", params)
            results = data.get("results", [])[:limit]

            for movie in results:
                movie["full_details"] = self.get_movie_details(movie["id"])

            return results
        except Exception as e:
            print(f"❌ Error fetching top-rated: {e}", file=sys.stderr)
            return []

    def get_now_playing(self, region: str = "US", limit: int = 10) -> List[Dict]:
        """
        Get movies currently in theaters

        Args:
            region: Country code
            limit: Maximum results

        Returns:
            List of currently playing movies
        """
        try:
            params = {"region": region, "page": 1}
            data = self._make_request("movie/now_playing", params)
            results = data.get("results", [])[:limit]

            for movie in results:
                movie["full_details"] = self.get_movie_details(movie["id"])

            return results
        except Exception as e:
            print(f"❌ Error fetching now playing: {e}", file=sys.stderr)
            return []

    def format_movie_list(self, movies: List[Dict], detailed: bool = True) -> str:
        """
        Format list of movies for display

        Args:
            movies: List of movie dictionaries
            detailed: Include full details (ratings, cast, etc.)

        Returns:
            Formatted string
        """
        if not movies:
            return "🎬 No movies found."

        output = []
        for i, movie in enumerate(movies, 1):
            details = movie.get("full_details", {})

            # Basic info
            title = movie.get("title", "Unknown")
            year = movie.get("release_date", "").split("-")[0] if movie.get("release_date") else "N/A"
            rating = details.get("vote_average", 0)
            vote_count = details.get("vote_count", 0)

            line = f"{i}. **{title}** ({year})"
            if detailed:
                output.append(line)
                output.append(f"   ⭐ Rating: {rating:.1f}/10 ({vote_count:,} votes)")

                # Runtime
                if details.get("runtime"):
                    hours = details["runtime"] // 60
                    mins = details["runtime"] % 60
                    output.append(f"   ⏱️  Runtime: {hours}h {mins}m")

                # Genres
                genres = [g["name"] for g in details.get("genres", [])]
                if genres:
                    output.append(f"   🎭 Genres: {', '.join(genres)}")

                # Top cast
                cast = details.get("credits", {}).get("cast", [])[:3]
                if cast:
                    cast_names = [c["name"] for c in cast]
                    output.append(f"   🎬 Cast: {', '.join(cast_names)}")

                # Director
                crew = details.get("credits", {}).get("crew", [])
                director = next((c["name"] for c in crew if c["job"] == "Director"), None)
                if director:
                    output.append(f"   🎥 Director: {director}")

                # Overview
                overview = details.get("overview", "").strip()
                if overview:
                    output.append(f"   📝 {overview[:200]}{'...' if len(overview) > 200 else ''}")

                output.append("")  # Empty line between movies
            else:
                line += f" - ⭐ {rating:.1f}/10"
                output.append(line)

        return "\n".join(output)


def main():
    """CLI entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 movie_search.py <command> [args]", file=sys.stderr)
        print("\nCommands:", file=sys.stderr)
        print("  latest [region] [days]  - Latest releases (default: US, 30 days)", file=sys.stderr)
        print("  search <query> [year]   - Search for movies", file=sys.stderr)
        print("  top-rated [region]      - Top-rated movies", file=sys.stderr)
        print("  now-playing [region]    - Currently in theaters", file=sys.stderr)
        print("\nExamples:", file=sys.stderr)
        print("  python3 movie_search.py latest US 30", file=sys.stderr)
        print("  python3 movie_search.py search \"Dune\" 2024", file=sys.stderr)
        print("  python3 movie_search.py top-rated US", file=sys.stderr)
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        searcher = MovieSearcher()

        if command == "latest":
            region = sys.argv[2] if len(sys.argv) > 2 else "US"
            days = int(sys.argv[3]) if len(sys.argv) > 3 else 30
            movies = searcher.get_latest_releases(region, days)
            print(searcher.format_movie_list(movies))

        elif command == "search":
            query = sys.argv[2]
            year = int(sys.argv[3]) if len(sys.argv) > 3 else None
            movies = searcher.search_movies(query, year)
            print(searcher.format_movie_list(movies))

        elif command == "top-rated":
            region = sys.argv[2] if len(sys.argv) > 2 else "US"
            movies = searcher.get_top_rated(region)
            print(searcher.format_movie_list(movies))

        elif command == "now-playing":
            region = sys.argv[2] if len(sys.argv) > 2 else "US"
            movies = searcher.get_now_playing(region)
            print(searcher.format_movie_list(movies))

        else:
            print(f"❌ Unknown command: {command}", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
