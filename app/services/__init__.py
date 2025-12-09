"""
Services module - HTTP client, scraper, cache
"""

from app.services.http_client import (  # noqa: F401
    fetch_json,
    fetch_html,
    close_client,
)
from app.services.scraper import (  # noqa: F401
    scrape_movies_page,
    parse_movies_from_html,
    close_pool,
)
from app.services.cache import cached, close_redis  # noqa: F401
