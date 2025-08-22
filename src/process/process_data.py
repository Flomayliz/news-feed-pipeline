"""
Helpers to clean and preprocess article data.
"""

import re
import requests
from bs4 import BeautifulSoup
from src.schemas import ArticleEntry
from pandas import DataFrame as df
from prefect import get_run_logger
from src.core import get_topics, get_keywords, get_settings


def _fetch_text_from_url(url: str) -> str:
    """
    Scrap text content from a web page.
    NOTE: This process may be slow and most servers block scraping attempts.
    
    Args:
        url (str): The URL of the web page to scrape.

    Returns:
        str: The text content of the web page, or None if an error occurred.
    """
    
    try:
        # Try to avoid simple blocks by adding a user-agent header
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=1)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return soup.get_text(separator=" ", strip=True)
    except requests.exceptions.RequestException as e:
        logger = get_run_logger()
        logger.debug(f"Error fetching URL {url}: {e}")
        return None


def _score_keywords(keywords, text) -> int:
    """
    Score the presence of keywords in the given text.
    This mechanism uses regular expressions to find whole words only, avoiding partial matches.
    
    Args:
        keywords (list): A list of keywords to search for.
        text (str): The text to search within.

    Returns:
        int: The score representing the presence of keywords in the text.

    """
    
    if not text or not keywords:
        return 0
    txt = str(text).lower()
    total = 0
    for term in keywords:
        if not term:
            continue
        pat = rf"(?<!\w){re.escape(term.lower())}(?!\w)"  # word-boundary-friendly for phrases
        total += len(re.findall(pat, txt))
    return total


def _raw_articles_to_df(articles: list[ArticleEntry]) -> df:
    """
    Convert a list of raw articles to a pandas DataFrame.
    """
    
    logger = get_run_logger()
    logger.info(f"Converting {len(articles)} raw articles to DataFrame")
    data = [article.model_dump() for article in articles]
    df_data = df(data)
    return df_data


def _remove_incomplete_articles(articles_df: df) -> df:
    """
    Remove articles with missing or incomplete information.
    """
    
    logger = get_run_logger()
    articles_df = articles_df.dropna().reset_index(drop=True)

    # Remove articles with empty columns
    articles_df = articles_df[articles_df["content_head"].str.strip() != ""]
    articles_df = articles_df[articles_df["title"].str.strip() != ""]
    articles_df = articles_df[articles_df["author"].str.strip() != ""]
    articles_df = articles_df[articles_df["description"].str.strip() != ""]
    articles_df = articles_df[articles_df["url"].str.strip() != ""]
    articles_df = articles_df[articles_df['source'].str.strip() != ""]

    logger.info(f"After removing incomplete articles, remaining articles: {len(articles_df)}")

    return articles_df


def _filter_articles(articles_df: df) -> df:
    """
    Filter articles based on content size and title length.
    """
    
    logger = get_run_logger()
    settings = get_settings()

    # Remove all articles with insufficient content size or title length
    articles_df = articles_df[articles_df["content_size"] >= settings.min_content_size]
    articles_df = articles_df[articles_df["title"].str.len() >= settings.min_title_size]

    logger.info(f"After filtering, remaining articles: {len(articles_df)}")

    # Remove all html tags from content, description and title
    articles_df["content_head"] = articles_df["content_head"].str.replace(
        r"<.*?>", "", regex=True
    )
    articles_df["description"] = articles_df["description"].str.replace(
        r"<.*?>", "", regex=True
    )
    articles_df["title"] = articles_df["title"].str.replace(r"<.*?>", "", regex=True)

    return articles_df


def _get_full_text(row):
    """
    Get article text to be evaluated for relevance.
    """
    
    settings = get_settings()
    
    # Only scrap the URLs if it explicit defined
    if not settings.get_full_text:
        text = ""
    else:
        text = _fetch_text_from_url(row["url"])

    if text is None or len(text.strip()) == 0:
        # Fallback to title + description + content_head
        return f"{row.get('title', '')} {row.get('description', '')} {row.get('content_head', '')}"
    return text


def _classify_articles(articles_df: df) -> df:
    """
    Classify articles into topics based on their content.

    It gives a score to each topic based on the presence of keywords.
    Each topic has a list of related topics to use in the classification.
    """
    logger = get_run_logger()
    # Check if required columns exist
    required_columns = ["url", "title"]
    missing_columns = [
        col for col in required_columns if col not in articles_df.columns
    ]
    if missing_columns:
        raise ValueError(f"Missing required columns for enrichment: {missing_columns}")

    # Fetch full text content for each article
    logger.info("Fetching full text content from article URLs")
    articles_df["full_text"] = articles_df.apply(_get_full_text, axis=1)

    # Count articles where text fetching failed
    fetch_failed = articles_df["full_text"].str.len() == 0
    if fetch_failed.any():
        logger.warning(f"Failed to fetch text for {fetch_failed.sum()} articles")

    # Calculate scores for each topic
    for topic in get_topics():
        keywords = get_keywords(topic)
        column_name = f"{topic}_score"
        logger.info(f"Calculating scores for topic: {topic}")
        articles_df[column_name] = articles_df.apply(
            lambda row: _score_keywords(keywords, f"{row['title']} {row['full_text']}"),
            axis=1,
        )

    return articles_df


def _df_to_article_entries(articles_df: df) -> list[ArticleEntry]:
    """
    Converts a DataFrame to a list of ArticleEntry objects, populating topics based on scores.
    """
    article_entries = []
    topics = get_topics()
    settings = get_settings()

    # Get the original fields from the ArticleEntry model to filter DataFrame columns
    article_fields = ArticleEntry.model_fields.keys()

    for _, row in articles_df.iterrows():
        article_topics = []
        for topic in topics:
            score_col = f"{topic}_score"
            if score_col in row and row[score_col] >= settings.score_threshold:
                article_topics.append(topic)

        # Create a dictionary with only the fields that belong to ArticleEntry
        article_data = row.to_dict()
        filtered_data = {
            key: article_data[key] for key in article_fields if key in article_data
        }
        filtered_data["topics"] = article_topics

        article_entries.append(ArticleEntry(**filtered_data))

    return article_entries


def process_data(raw_articles: list[ArticleEntry]) -> list[ArticleEntry]:
    """
    Run all the filtering and classification steps on the raw articles.
    """
    
    articles_df = _raw_articles_to_df(raw_articles)
    if articles_df.empty:
        return []
    articles_df = _remove_incomplete_articles(articles_df)
    articles_df = _filter_articles(articles_df)
    articles_df = _classify_articles(articles_df)
    article_entries = _df_to_article_entries(articles_df)
    return article_entries
