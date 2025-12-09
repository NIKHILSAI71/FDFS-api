"""
BookMyShow Fast API - Main Application
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core import config
from app.core.security import limiter
from app.services import close_client, close_pool, close_redis
from app.routes import regions_router, search_router, theaters_router, movies_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle."""
    yield
    await close_client()
    await close_pool()
    await close_redis()

app = FastAPI(
    title="FDFS - First Day First Show API",
    description="High-performance movie booking API powered by BookMyShow data",
    version="1.0.0",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(regions_router)
app.include_router(search_router)
app.include_router(theaters_router)
app.include_router(movies_router)

@app.get("/", tags=["Health"])
async def health_check():
    return {"status": "ok", "message": "FDFS - First Day First Show API is running"}

@app.get("/health", tags=["Health"])
async def detailed_health():
    return {"status": "ok", "version": "1.0.0"}
