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

    movie_blocks = re.findall(
        r'data-entity-id="([^"]+)"[^>]*data-entity-name="([^"]+)"', html
    )

    for entity_id, entity_name in movie_blocks:
        movies.append({"id": entity_id, "name": entity_name, "type": movie_type})

    if not movies:
        json_ld_pattern = r'<script type="application/ld\+json">(.*?)</script>'
        json_matches = re.findall(json_ld_pattern, html, re.DOTALL)

        for json_str in json_matches:
            try:
                data = json.loads(json_str)
                if isinstance(data, dict) and data.get("@type") == "Movie":
                    movies.append(
                        {
                            "id": data.get("identifier", ""),
                            "name": data.get("name", ""),
                            "type": movie_type,
                        }
                    )
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and item.get("@type") == "Movie":
                            movies.append(
                                {
                                    "id": item.get("identifier", ""),
                                    "name": item.get("name", ""),
                                    "type": movie_type,
                                }
                            )
            except json.JSONDecodeError:
                pass

    return movies


async def close_pool():
    """No cleanup needed."""
    pass
