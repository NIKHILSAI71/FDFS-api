"""
Scraper service for parsing HTML content.
"""

import re
import json
from typing import List, Dict
from app.services.http_client import fetch_html


async def scrape_movies_page(url: str) -> str:
    """Fetch a movies page HTML content."""
    return await fetch_html(url)


def parse_movies_from_html(html: str, movie_type: str) -> List[Dict]:
    """Parse movie data from HTML content."""
    movies = []
    seen_ids = set()

    # Primary pattern: Extract from movie card links /movies/{slug}/{id}
    movie_links = re.findall(r'href="/movies/([^/]+)/(ET\d+)"', html)

    for slug, movie_id in movie_links:
        if movie_id in seen_ids:
            continue
        seen_ids.add(movie_id)

        # Try to find the movie name nearby in the HTML
        name = slug.replace("-", " ").title()

        movies.append(
            {
                "id": movie_id,
                "name": name,
                "slug": slug,
                "type": movie_type,
                "poster": (
                    f"https://assets-in.bmscdn.com/discovery-catalog/events/"
                    f"tr:w-400,h-600,bg-CCCCCC/{movie_id.lower()}-portrait.jpg"
                ),
                "booking_url": f"https://in.bookmyshow.com/movies/{slug}/{movie_id}",
            }
        )

    # Secondary pattern: Extract from paths like /movies/{slug} with ET code nearby
    if not movies:
        # Find all movie slugs and ET codes
        movie_slugs = re.findall(r'/movies/([a-z0-9-]+)(?:/|")', html)
        et_codes = re.findall(r"(ET\d{8})", html)

        # Create unique sets
        unique_slugs = list(dict.fromkeys(movie_slugs))[:30]  # Keep order, limit to 30
        unique_et_codes = list(dict.fromkeys(et_codes))

        # Match slugs with ET codes (they appear in same order)
        for i, slug in enumerate(unique_slugs):
            if slug in ["upcoming", "now-playing", "coming-soon", "movies"]:
                continue
            movie_id = (
                unique_et_codes[i] if i < len(unique_et_codes) else f"UNKNOWN-{i}"
            )
            if movie_id in seen_ids:
                continue
            seen_ids.add(movie_id)

            name = slug.replace("-", " ").title()
            movies.append(
                {
                    "id": movie_id,
                    "name": name,
                    "slug": slug,
                    "type": movie_type,
                    "poster": (
                        f"https://assets-in.bmscdn.com/discovery-catalog/events/"
                        f"tr:w-400,h-600,bg-CCCCCC/{movie_id.lower()}-portrait.jpg"
                    ),
                    "booking_url": f"https://in.bookmyshow.com/movies/{slug}/{movie_id}",
                }
            )

    # Fallback: Try JSON-LD data
    if not movies:
        json_ld_pattern = r'<script type="application/ld\+json">(.*?)</script>'
        json_matches = re.findall(json_ld_pattern, html, re.DOTALL)

        for json_str in json_matches:
            try:
                data = json.loads(json_str)
                if isinstance(data, dict) and data.get("@type") == "Movie":
                    movie_id = data.get("identifier", "")
                    if movie_id and movie_id not in seen_ids:
                        seen_ids.add(movie_id)
                        movies.append(
                            {
                                "id": movie_id,
                                "name": data.get("name", ""),
                                "slug": (
                                    data.get("url", "").split("/")[-2]
                                    if data.get("url")
                                    else ""
                                ),
                                "type": movie_type,
                            }
                        )
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("@type") == "Movie":
                            movie_id = item.get("identifier", "")
                            if movie_id and movie_id not in seen_ids:
                                seen_ids.add(movie_id)
                                movies.append(
                                    {
                                        "id": movie_id,
                                        "name": item.get("name", ""),
                                        "slug": (
                                            item.get("url", "").split("/")[-2]
                                            if item.get("url")
                                            else ""
                                        ),
                                        "type": movie_type,
                                    }
                                )
            except json.JSONDecodeError:
                pass

    return movies


async def close_pool():
    """No cleanup needed."""
    pass
