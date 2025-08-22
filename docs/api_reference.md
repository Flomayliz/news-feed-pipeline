# API Reference

This document provides a comprehensive reference for the News Feed Pipeline API endpoints.

## Base URL

All API endpoints are served under the base URL: `http://localhost:8000/api`


## Endpoints

### GET /api/get_topics

Returns a list of all available topics in the news feed.

**Request Example:**
```bash
curl http://localhost:8000/api/get_topics
```

**Response:**
```json
["ai", "marketing", "science"]
```

**Status Codes:**
- `200 OK`: Topics successfully retrieved
- `500 Internal Server Error`: Server error occurred

---

### GET /api/get_news_by_topic

Returns news articles filtered by the specified parameters.

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `topics` | array | No | List of topics to filter articles by (default: all topics) |
| `limit` | integer | No | Maximum number of articles to return (default: 10) |
| `from_date` | datetime | No | Start date for articles (default: 7 days ago) |
| `to_date` | datetime | No | End date for articles (default: current date) |
| `sort_by_match` | boolean | No | Whether to sort by topic match relevance (default: false) |

**Request Example:**
```bash
curl "http://localhost:8000/api/get_news_by_topic?topics=ai&limit=5&sort_by_match=true"
```

**Response:**
```json
[
  {
    "author": "Jane Doe",
    "title": "Latest in AI Technology",
    "description": "A look at recent AI advances",
    "url": "https://example.com/article",
    "published_at": "2025-08-21T15:30:00Z",
    "content_head": "The latest developments in AI...",
    "content_size": 4500,
    "source": "Tech News Daily",
    "topics": ["ai"]
  },
  {
    "author": "John Smith",
    "title": "Machine Learning Breakthroughs",
    "description": "Recent advances in ML algorithms",
    "url": "https://example.com/article2",
    "published_at": "2025-08-20T10:15:00Z",
    "content_head": "Machine learning algorithms have seen significant...",
    "content_size": 3800,
    "source": "AI Today",
    "topics": ["ai"]
  }
]
```

**Status Codes:**
- `200 OK`: Articles successfully retrieved
- `400 Bad Request`: Invalid parameters provided
- `500 Internal Server Error`: Server error occurred

**Error Response Example:**
```json
{
  "detail": "Invalid date format. Use ISO format (YYYY-MM-DD)"
}
```

## Data Models

### Article

| Field | Type | Description |
|-------|------|-------------|
| `author` | string | Article author's name |
| `title` | string | Article title |
| `description` | string | Short description or summary of the article |
| `url` | string | Original URL to the article |
| `published_at` | datetime | Publication date and time in ISO format |
| `content_head` | string | Beginning of the article content |
| `content_size` | integer | Size of the article content in characters |
| `source` | string | Name of the source publication |
| `topics` | array | List of topics associated with the article |

## Rate Limiting

To prevent abuse, the API implements rate limiting of 100 requests per hour per IP address.

## Interactive Documentation

FastAPI provides an interactive documentation interface that allows you to explore and test the API:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`


## Implementation Details

The API is implemented using FastAPI and connects to MongoDB to fetch the processed news articles. The source code for the API implementation can be found in `src/api/main.py`.
