from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core import config

# API Key Authentication
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Validate API key from header."""
    if api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Include 'X-API-Key' header.",
        )
    if api_key not in config.API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API key."
        )
    return api_key


# Rate Limiter
limiter = Limiter(key_func=get_remote_address)


def get_limiter() -> Limiter:
    return limiter
