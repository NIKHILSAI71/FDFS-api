from fastapi import APIRouter, Depends, Request
from app.core.security import verify_api_key, limiter
from app.core import config
from app.services.http_client import fetch_json
from app.services.cache import cached

router = APIRouter(tags=["Regions"])


@router.get("/regions")
@limiter.limit(config.RATE_LIMIT)
async def get_regions(request: Request, api_key: str = Depends(verify_api_key)):
    """Get all available regions and cities."""
    return await _fetch_regions()


@cached("regions", ttl=config.CACHE_TTL_REGIONS)
async def _fetch_regions():
    url = f"{config.BMS_BASE_URL}/api/explore/v1/discover/regions"
    data = await fetch_json(url)

    regions = []
    if "BookMyShow" in data:
        for city in data["BookMyShow"].get("TopCities", []):
            regions.append(
                {
                    "code": city.get("RegionCode"),
                    "name": city.get("RegionName"),
                    "slug": city.get("RegionSlug"),
                    "alias": city.get("Alias"),
                }
            )
        for city in data["BookMyShow"].get("OtherCities", []):
            regions.append(
                {
                    "code": city.get("RegionCode"),
                    "name": city.get("RegionName"),
                    "slug": city.get("RegionSlug"),
                    "alias": city.get("Alias"),
                }
            )

    return {"regions": regions, "count": len(regions)}
