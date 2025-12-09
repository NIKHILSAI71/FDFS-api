from fastapi import APIRouter, Depends, Query, Request
from app.core.security import verify_api_key, limiter
from app.core import config
from app.services.http_client import fetch_json
from app.services.cache import cached

router = APIRouter(tags=["Theaters"])


@router.get("/theaters")
@limiter.limit(config.RATE_LIMIT)
async def get_theaters(
    request: Request,
    region: str = Query(..., description="Region code (e.g., HYD, MUMBAI)"),
    api_key: str = Depends(verify_api_key),
):
    """Get all theaters/cinemas in a region."""
    return await _fetch_theaters(region=region)


@cached("theaters", ttl=config.CACHE_TTL_THEATERS)
async def _fetch_theaters(region: str):
    url = f"{config.BMS_BASE_URL}/api/v2/mobile/venues"
    data = await fetch_json(url, params={"regionCode": region, "eventType": "MT"})

    theaters = []
    for venue in data.get("venues", []):
        venue_code = venue.get("VenueCode", "")
        venue_name = venue.get("VenueName", "Unknown")
        city = venue.get("City", "")
        state = venue.get("State", "")

        latitude = venue.get("VenueLatitude")
        longitude = venue.get("VenueLongitude")
        try:
            latitude = float(latitude) if latitude else None
            longitude = float(longitude) if longitude else None
        except (ValueError, TypeError):
            latitude, longitude = None, None

        theaters.append(
            {
                "code": venue_code,
                "name": venue_name,
                "address": venue.get("VenueAddress", ""),
                "city": city,
                "state": state,
                "country": venue.get("Country", "India"),
                "postal_code": venue.get("PostalCode", ""),
                "latitude": latitude,
                "longitude": longitude,
                "region_code": venue.get("RegionCode", region),
                "is_new": venue.get("CinemaIsNew", "N") == "Y",
                "has_mobile_tickets": venue.get("MTicket", "N") == "Y",
                "has_food_sales": venue.get("FoodSales", "N") == "Y",
                "facilities": venue.get("VenueLegends", "").replace(";", " ").strip(),
                "formats": venue.get("availableEventFormats", ""),
                "cinema_url": (
                    f"{config.BMS_BASE_URL}/venue/{venue_code}" if venue_code else None
                ),
            }
        )

    return {"theaters": theaters, "count": len(theaters), "region": region}
