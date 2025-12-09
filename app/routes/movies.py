from fastapi import APIRouter, Depends, Query, Request
from app.core.security import verify_api_key, limiter
from app.core import config
from app.services.scraper import scrape_movies_page, parse_movies_from_html
from app.services.cache import cached

router = APIRouter(tags=["Movies"])

@router.get("/now-showing")
@limiter.limit(config.RATE_LIMIT)
async def get_now_showing(
    request: Request,
    region: str = Query(..., description="Region slug (e.g., hyderabad, mumbai)"),
    api_key: str = Depends(verify_api_key)
):
    """Get currently showing movies in a region."""
    return await _fetch_now_showing(region=region)

@router.get("/upcoming")
@limiter.limit(config.RATE_LIMIT)
async def get_upcoming(
    request: Request,
    region: str = Query(..., description="Region slug (e.g., hyderabad, mumbai)"),
    api_key: str = Depends(verify_api_key)
):
    """Get upcoming movies in a region."""
    return await _fetch_upcoming(region=region)

@cached("now_showing", ttl=config.CACHE_TTL_MOVIES)
async def _fetch_now_showing(region: str):
    url = f"{config.BMS_BASE_URL}/{region}/movies"
    html = await scrape_movies_page(url)
    movies = parse_movies_from_html(html, "now_showing")
    return {"movies": movies, "count": len(movies), "region": region, "type": "now_showing"}

@cached("upcoming", ttl=config.CACHE_TTL_MOVIES)
async def _fetch_upcoming(region: str):
    url = f"{config.BMS_BASE_URL}/{region}/movies/upcoming"
    html = await scrape_movies_page(url)
    movies = parse_movies_from_html(html, "upcoming")
    return {"movies": movies, "count": len(movies), "region": region, "type": "upcoming"}
