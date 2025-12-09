# Deploy

Production deployment files for BookMyShow API.

## Docker

```bash
# Build and run
cd deploy
docker-compose up -d

# View logs
docker-compose logs -f api
```

## Manual

```bash
# Install
pip install -r requirements.txt gunicorn

# Run with gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```
