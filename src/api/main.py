from fastapi import FastAPI, Query
from typing import List, Optional
from datetime import datetime
from src.schemas.schemas import ArticleEntry
from src.persistence.database import DataPersistence
from src.persistence.factory import get_database
from src.core import get_topics
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="News API",
    description="API for fetching news articles by topic.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="src/api/html/static"), name="static")

# CORS (optional; same-origin usually fine). Adjust origins if necessary.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

data_persistence: DataPersistence = get_database()  # You may need to adjust this


@app.get("/", include_in_schema=False)
async def root_page():
    # Serves the frontend (index.html at project root)
    return FileResponse("src/api/html/index.html")


@app.get("/api/get_topics", response_model=List[str])
async def api_get_topics():
    return get_topics()


@app.get("/api/get_news_by_topic", response_model=List[ArticleEntry], tags=["news"])
def api_get_news_by_topic(
    topics: List[str] = Query([], description="List of topics to filter articles"),
    limit: int = Query(10, description="Number of articles to return"),
    from_date: Optional[datetime] = Query(None, description="Start date for articles"),
    to_date: Optional[datetime] = Query(None, description="End date for articles"),
    sort_by_match: bool = Query(False, description="Order by topic match"),
):
    articles = data_persistence.get_matching_articles(
        topics=topics,
        from_date=from_date,
        to_date=to_date,
        sort_by_match=sort_by_match,
        limit=limit,
    )
    return [article.model_dump() for article in articles]


# Health check endpoint
@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}


# Root endpoint
@app.get("/", tags=["system"])
def root():
    return {"message": "Welcome to Dentu News API. Use /get_news_by_topic to fetch articles."}
