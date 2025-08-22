"""
News pipeline flow for fetching, processing, and storing news articles.
"""

from src.fetch import get_fetcher
from src.persistence import get_database
from src.process import process_data
from src.core import get_topics
from prefect import flow, task, get_run_logger
from datetime import datetime, timedelta
from typing import List
from src.schemas import ArticleEntry


@task
def get_keywords_from_topics() -> List[str]:
    """Get all available topics as keywords."""
    logger = get_run_logger()
    topics = get_topics()
    logger.info(f"Retrieved {len(topics)} topics as keywords: {topics}")
    return topics


@task
def fetch_news_data(
    fetcher, keywords: List[str], from_date: datetime, to_date: datetime
) -> dict:
    """Task to fetch raw news data."""
    logger = get_run_logger()
    logger.info(f"Fetching data with keywords: {keywords}")
    return fetcher.fetch_data(keywords=keywords, from_date=from_date, to_date=to_date)


@task
def parse_news_articles(fetcher, raw_data: dict):
    """Task to parse articles from raw data."""
    logger = get_run_logger()
    logger.info("Parsing articles from raw data")
    return fetcher.parse_articles(raw_data)


@task
def process_articles_task(parsed_articles) -> list[ArticleEntry]:
    """Task to process articles."""
    logger = get_run_logger()
    if parsed_articles:
        logger.info(f"Processing {len(parsed_articles)} articles")
        return process_data(parsed_articles)
    else:
        logger.info("No parsed articles")
        return []


@task
def store_articles_task(articles) -> int:
    """Task to store articles in the database."""
    logger = get_run_logger()
    if articles:
        logger.info(f"Storing {len(articles)} articles in database")
        db = get_database()
        db.store_articles(articles)
        stored_count = len(articles)
        logger.info(f"Successfully stored {stored_count} articles")
        return stored_count
    else:
        logger.warning("No articles to store")
        return 0


@flow(name="news_pipeline_flow")
def news_pipeline_flow(hours_back: int = 24):
    """
    Simplified news data pipeline flow that runs every N hours.

    Args:
        hours_back: Number of hours to look back for news (default: 24)
                   Note: Due to API constraints, we add 24h offset to get older news

    Returns:
        Number of articles successfully stored.
    """
    logger = get_run_logger()
    logger.info(f"Starting news pipeline flow - looking back {hours_back} hours")

    try:
        # Calculate date range with 24h offset for API constraints
        now = datetime.now()
        # End date: 24 hours ago (API constraint)
        to_date = now - timedelta(hours=24)
        # Start date: hours_back + 24 hours ago
        from_date = now - timedelta(hours=24 + hours_back)

        logger.info(f"Fetching news from {from_date} to {to_date} (24h offset applied)")

        # Initialize components
        logger.info("Initializing fetcher and database")
        fetcher = get_fetcher()

        # Get keywords from topics
        keywords = get_keywords_from_topics()

        # Fetch and process data
        raw_data = fetch_news_data(fetcher, keywords, from_date, to_date)

        parsed_articles = parse_news_articles(fetcher, raw_data)

        logger.info(f"Processing and enriching {len(parsed_articles)} articles")
        enriched_articles = process_articles_task(parsed_articles)

        # Store articles using task
        stored_count = store_articles_task(enriched_articles)

        logger.info(
            f"Pipeline completed successfully. Processed {len(parsed_articles)} raw articles, stored {stored_count} enriched articles."
        )
        return stored_count

    except Exception as e:
        logger.error(f"Pipeline failed with error: {str(e)}")
        raise


if __name__ == "__main__":
    # Example usage - fetch last 12 hours of news (with 24h offset)
    result = news_pipeline_flow(hours_back=12)
    print(f"Pipeline completed: {result} articles stored")
