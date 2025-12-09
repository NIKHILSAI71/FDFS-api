from fastapi import APIRouter, Depends, Query, Request
from app.core.security import verify_api_key, limiter
from app.core import config
from app.services.http_client import fetch_json
from app.services.cache import cached
from urllib.parse import quote

router = APIRouter(tags=["Search"])


@router.get("/search")
@limiter.limit(config.RATE_LIMIT)
async def search_movies(
    request: Request,
    q: str = Query(..., min_length=1, description="Search query"),
    api_key: str = Depends(verify_api_key),
):
    """Search for movies by name."""
    return await _search_movies(query=q)


@cached("search", ttl=config.CACHE_TTL_SEARCH)
async def _search_movies(query: str):
    encoded_query = quote(query)
    url = f"{config.BMS_BASE_URL}/quickbook-search.bms?cat=MT&q={encoded_query}"

    data = await fetch_json(url)
    movies = []

    for item in data.get("hits", []):
        if item.get("TYPE") != "MT":
            continue

        movie_id = item.get("ID", "")
        movie_slug = item.get("SLUG", "")
        movie_title = item.get("TITLE") or item.get("GROUP_TITLE") or "Unknown"

        booking_url = (
            f"{config.BMS_BASE_URL}/movies/{movie_slug}/{movie_id}"
            if movie_slug and movie_id
            else ""
        )

        movies.append(
            {
                "id": movie_id,
                "code": item.get("CODE", ""),
                "name": movie_title,
                "slug": movie_slug,
                "poster": item.get("POSTER_URL", ""),
                "release_date": item.get("RDATE", ""),
                "status": item.get("ST", ""),
                "is_streaming": item.get("IS_STREAM", False),
                "is_online": item.get("IS_ONLINE", False),
                "region": item.get("REGION_SLUG", ""),
                "booking_url": booking_url,
            }
        )

    return {"movies": movies, "count": len(movies), "query": query}
