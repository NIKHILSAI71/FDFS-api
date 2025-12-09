"""
MCP Server for BookMyShow API
Exposes movie search, theaters, and showtimes as AI tools.
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from app.core import config
from app.services.http_client import fetch_json, fetch_html
from app.services.scraper import parse_movies_from_html

# Create MCP server
app = Server("fdfs")

TOOLS = [
    Tool(
        name="get_regions",
        description="Get all BookMyShow regions/cities in India",
        inputSchema={"type": "object", "properties": {}, "required": []},
    ),
    Tool(
        name="search_movies",
        description="Search for movies by name",
        inputSchema={
            "type": "object",
            "properties": {"query": {"type": "string", "description": "Movie name"}},
            "required": ["query"],
        },
    ),
    Tool(
        name="get_theaters",
        description="Get theaters in a region",
        inputSchema={
            "type": "object",
            "properties": {
                "region_code": {
                    "type": "string",
                    "description": "Region code (HYD, MUMBAI)",
                }
            },
            "required": ["region_code"],
        },
    ),
    Tool(
        name="get_now_showing",
        description="Get currently showing movies",
        inputSchema={
            "type": "object",
            "properties": {
                "region_slug": {
                    "type": "string",
                    "description": "Region slug (hyderabad)",
                }
            },
            "required": ["region_slug"],
        },
    ),
]


@app.list_tools()
async def list_tools() -> list[Tool]:
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    handlers = {
        "get_regions": _get_regions,
        "search_movies": lambda: _search_movies(arguments.get("query", "")),
        "get_theaters": lambda: _get_theaters(arguments.get("region_code", "")),
        "get_now_showing": lambda: _get_now_showing(arguments.get("region_slug", "")),
    }

    handler = handlers.get(name)
    result = await handler() if handler else {"error": f"Unknown tool: {name}"}

    return [TextContent(type="text", text=json.dumps(result, indent=2))]


async def _get_regions() -> dict:
    url = f"{config.BMS_BASE_URL}/api/explore/v1/discover/regions"
    data = await fetch_json(url)
    regions = []
    if "BookMyShow" in data:
        for city in data["BookMyShow"].get("TopCities", [])[:30]:
            regions.append(
                {"code": city.get("RegionCode"), "name": city.get("RegionName")}
            )
    return {"regions": regions, "count": len(regions)}


async def _search_movies(query: str) -> dict:
    from urllib.parse import quote

    url = f"{config.BMS_BASE_URL}/quickbook-search.bms?cat=MT&q={quote(query)}"
    data = await fetch_json(url)
    movies = [
        {"name": h.get("TITLE"), "id": h.get("ID")}
        for h in data.get("hits", [])[:10]
        if h.get("TYPE") == "MT"
    ]
    return {"movies": movies, "query": query}


async def _get_theaters(region_code: str) -> dict:
    url = f"{config.BMS_BASE_URL}/api/v2/mobile/venues"
    data = await fetch_json(url, params={"regionCode": region_code, "eventType": "MT"})
    theaters = [
        {"name": v.get("VenueName"), "code": v.get("VenueCode")}
        for v in data.get("venues", [])[:20]
    ]
    return {"theaters": theaters, "region": region_code}


async def _get_now_showing(region_slug: str) -> dict:
    url = f"{config.BMS_BASE_URL}/{region_slug}/movies"
    html = await fetch_html(url)
    movies = parse_movies_from_html(html, "now_showing")[:15]
    return {"movies": movies, "region": region_slug}


async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
