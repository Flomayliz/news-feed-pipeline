# Advanced Configuration

This document provides detailed guidance on customizing and configuring the News Feed Pipeline beyond the basic setup.

## Environment Variables

All configuration is managed through environment variables or a `.env` file. Below is a comprehensive list of available settings:

| Variable | Description | Default | Example |
|----------|-------------|---------|---------|
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017` | `mongodb+srv://user:password@cluster.mongodb.net` |
| `MONGO_DB_NAME` | MongoDB database name | `ai_news_feed` | `production_news` |
| `NEWS_API_KEY` | API key for NewsAPI access | - | `your_api_key` |
| `MIN_CONTENT_SIZE` | Minimum content size in bytes | `1000` | `2000` |
| `MIN_TITLE_SIZE` | Minimum title length | `15` | `20` |
| `SCORE_THRESHOLD` | Threshold for topic classification | `2` | `3` |
| `GET_FULL_TEXT` | Whether to fetch full article text | `false` | `true` |

## Topic Management

The system classifies news articles into topics based on keywords defined in `src/core/topic_dictionary.py`.

### Adding a New Topic

To add a new topic with its keywords:

1. Open `src/core/topic_dictionary.py`
2. Add a new entry to the `TOPIC_KEYWORDS` dictionary:

```python
TOPIC_KEYWORDS = {
    # existing topics...
    "technology": [
        "tech",
        "gadget",
        "smartphone",
        "computer",
        "software",
        "hardware",
        # add more keywords...
    ],
}
```

### Modifying Topic Keywords

To modify the keywords for an existing topic:

1. Open `src/core/topic_dictionary.py`
2. Locate the topic in the `TOPIC_KEYWORDS` dictionary
3. Add, remove, or modify the keywords as needed

### Topic Classification Tuning

The system uses a simple keyword-based scoring mechanism to classify articles:

- Each occurrence of a topic's keyword adds 1 to the score for that topic
- Articles are tagged with topics whose score exceeds the `SCORE_THRESHOLD`

To adjust the sensitivity:

- **Increase `SCORE_THRESHOLD`** for stricter classification (fewer topics per article)
- **Decrease `SCORE_THRESHOLD`** for more liberal classification (more topics per article)

## API Configuration

### CORS Settings

By default, the API allows cross-origin requests from all origins. For production deployments, you should restrict this:

1. Open `src/api/main.py`
2. Modify the CORS middleware settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Restrict to your domain
    allow_credentials=True,
    allow_methods=["GET"],  # Restrict to necessary methods
    allow_headers=["*"],
)
```

### API Rate Limiting

The API doesn't include rate limiting by default. To add it:

1. Install the rate limiting dependency:
   ```bash
   pdm add fastapi-limiter
   ```

2. Implement rate limiting in `src/api/main.py`:
   ```python
   from fastapi_limiter import FastAPILimiter
   from fastapi_limiter.depends import RateLimiter
   
   @app.on_event("startup")
   async def startup():
       await FastAPILimiter.init(redis)
   
   @app.get("/api/get_news_by_topic", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
   def api_get_news_by_topic():
       # existing code...
   ```

## Performance Tuning

### Content Filtering

Adjust these settings to filter articles more or less aggressively:

- `MIN_CONTENT_SIZE`: Minimum size of article content in bytes
  - Increase to filter out shorter, potentially less informative articles
  - Decrease if you're not getting enough articles

- `MIN_TITLE_SIZE`: Minimum length of article titles
  - Increase to filter out articles with short, potentially clickbait titles
  - Decrease if you're losing too many valid articles

### Full Text Analysis

By default, the system only uses article snippets provided by the News API. For more accurate topic classification:

1. Set `GET_FULL_TEXT=true` in your `.env` file
2. Be aware this will:
   - Improve classification accuracy
   - Significantly slow down processing
   - May trigger rate limits or blocking from news sites

### MongoDB Indexing

For larger datasets, create appropriate indexes in MongoDB:

```javascript
// Index for topic-based queries
db.docs.createIndex({ "topics": 1 });

// Index for date-based queries
db.docs.createIndex({ "published_at": -1 });

// Compound index for topic + date queries
db.docs.createIndex({ "topics": 1, "published_at": -1 });
```

### Prefect Flow Configuration

Customize the pipeline execution by modifying `src/flows/news_pipeline.py`:

- **Fetch Window**: Adjust the `hours_back` parameter to fetch older or newer articles
- **Task Configuration**: Add retries or custom error handling to specific tasks
- **Scheduling**: Change the interval in `src/serve.py` (default: 10 minutes)

### Prefect Block Configuration

The application automatically creates a Prefect block to store configuration parameters if it doesn't exist. This enables dynamic configuration management through the Prefect UI.

#### How the Block System Works

1. **First-time Initialization**:
   - When the pipeline starts for the first time, it checks for the existence of a configuration block
   - If the block doesn't exist:
     - It retrieves configuration from environment variables (`.env` file)
     - If environment variables are not set, it uses default values
     - It creates a new configuration block with these values

2. **Subsequent Runs**:
   - The pipeline retrieves configuration from the Prefect block
   - Any changes made through the Prefect UI are automatically applied

3. **Updating Configuration**:
   - Navigate to the "Blocks" section in the Prefect UI (http://localhost:4200/blocks)
   - Find the "NewsFeedConfig" block
   - Edit the parameters and save changes
   - Changes take effect on the next flow run

#### Available Block Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `news_api_key` | API key for NewsAPI | From `.env` |
| `mongo_uri` | MongoDB connection string | From `.env` |
| `mongo_db_name` | MongoDB database name | From `.env` |
| `min_content_size` | Minimum content size in bytes | 1000 |
| `min_title_size` | Minimum title length | 15 |
| `score_threshold` | Topic classification threshold | 2 |
| `get_full_text` | Whether to fetch full article text | false |
| `hours_back` | How many hours back to fetch articles | 24 |
