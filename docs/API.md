# API Documentation

## FDFS - First Day First Show API

### Endpoints

#### GET /regions
Get all available regions/cities.

**Headers:** `X-API-Key: your-key`

**Response:**
```json
{
  "regions": [{"code": "HYD", "name": "Hyderabad", "slug": "hyderabad"}],
  "count": 1999
}
```

---

#### GET /search?q={query}
Search for movies by name.

**Parameters:**
- `q` (required): Search query

**Response:**
```json
{
  "movies": [{"id": "ET00471874", "name": "Pushpa 2", "slug": "pushpa-2", "poster": "..."}],
  "count": 8,
  "query": "pushpa"
}
```

---

#### GET /theaters?region={code}
Get theaters in a specific region.

**Parameters:**
- `region` (required): Region code (HYD, MUMBAI, BANG)

**Response:**
```json
{
  "theaters": [{"code": "AMBH", "name": "AMB Cinemas", "address": "...", "city": "Hyderabad"}],
  "count": 90,
  "region": "HYD"
}
```

---

#### GET /now-showing?region={slug}
Get currently showing movies.

---

#### GET /upcoming?region={slug}
Get upcoming movies.
