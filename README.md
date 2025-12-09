# FDFS - First Day First Show API

High-performance movie booking API powered by BookMyShow data with Cloudflare bypass.

## Features

- 🚀 **Fast** - curl-cffi for Cloudflare bypass
- 🔐 **Secure** - API key authentication + rate limiting
- 🤖 **AI Ready** - MCP server for Claude integration
- 🐳 **Docker** - Production-ready deployment

## Quick Start

```bash
# Clone
git clone https://github.com/yourusername/FDFS-API.git
cd FDFS-API

# Install
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload
```

## API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /regions` | List all cities |
| `GET /search?q=movie` | Search movies |
| `GET /theaters?region=HYD` | List theaters |
| `GET /now-showing?region=hyderabad` | Current movies |
| `GET /upcoming?region=hyderabad` | Upcoming movies |

## Authentication

All endpoints require an API key:

```bash
curl -H "X-API-Key: dev-key-123" http://localhost:8000/regions
```

## Project Structure

```
FDFS-API/
├── app/                 # Main application
│   ├── core/           # Config, security
│   ├── routes/         # API endpoints
│   └── services/       # HTTP client, cache
├── mcp/                # MCP server for AI
├── deploy/             # Docker files
├── docs/               # Documentation
└── .github/workflows/  # CI/CD
```

## Documentation

- [API Reference](docs/API.md)
- [MCP Integration](docs/MCP.md)
- [Deployment Guide](deploy/README.md)

## License

MIT
