import os
from dotenv import load_dotenv

load_dotenv()

# Server
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))
WORKERS = int(os.getenv("WORKERS", 4))

# Redis
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

# Cache TTL (seconds)
CACHE_TTL_REGIONS = 3600  # 1 hour
CACHE_TTL_MOVIES = 300  # 5 minutes
CACHE_TTL_THEATERS = 600  # 10 minutes
CACHE_TTL_SEARCH = 120  # 2 minutes

# Security
API_KEYS = set(os.getenv("API_KEYS", "dev-key-123").split(","))
RATE_LIMIT = os.getenv("RATE_LIMIT", "100/minute")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# BookMyShow
BMS_BASE_URL = "https://in.bookmyshow.com"
BMS_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9,hi;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://in.bookmyshow.com/explore/movies-hyderabad?cat=MT",
    "Origin": "https://in.bookmyshow.com",
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
}
