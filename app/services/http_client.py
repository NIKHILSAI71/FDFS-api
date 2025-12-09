"""
HTTP client with Cloudflare bypass using curl-cffi.
"""
import asyncio
from typing import Optional, Any
from curl_cffi import requests as cf_requests
from fastapi import HTTPException
from app.core import config

async def fetch_json(url: str, params: dict = None) -> dict:
    """Fetch JSON from URL using curl-cffi to bypass Cloudflare."""
    try:
        if params:
            param_str = "&".join(f"{k}={v}" for k, v in params.items())
            url = f"{url}?{param_str}"
        
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: cf_requests.get(
                url,
                impersonate="chrome120",
                headers=config.BMS_HEADERS,
                timeout=30
            )
        )
        
        if response.status_code == 403:
            raise HTTPException(status_code=503, detail="Cloudflare is blocking requests.")
        
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=f"API returned {response.status_code}")
        
        return response.json()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Request failed: {str(e)}")

async def fetch_html(url: str) -> str:
    """Fetch HTML content using curl-cffi."""
    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: cf_requests.get(
                url,
                impersonate="chrome120",
                headers=config.BMS_HEADERS,
                timeout=30
            )
        )
        
        if response.status_code == 403:
            raise HTTPException(status_code=503, detail="Cloudflare is blocking requests.")
        
        return response.text
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Request failed: {str(e)}")

async def close_client():
    """No cleanup needed for curl-cffi."""
    pass
