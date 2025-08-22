"""
News API Fetcher implementation.
"""

from src.fetch.fetcher import Fetcher
from src.schemas import ArticleEntry
from datetime import datetime
from typing import List
import requests
from src.core.config import get_settings
from prefect import get_run_logger


class NewsApiFetcher(Fetcher):
    """
    News API Fetcher implementation.

    This fetcher retrieves articles from newsapi.org.
    For more information, visit the 
    [News API documentation](https://newsapi.org/docs/getting-started).
    """

    # For this implementation, we only use the "everything" endpoint
    BASE_URL = "https://newsapi.org/v2/everything"

    # The complete value for the encoded keyword query must be
    # 500 char max according to the News API documentation.
    # We set a lower limit to allow for other URL parameters.
    MAX_KEYWORDS_QUERY_CHARS = 400

    def __init__(self, **kwargs):
        logger = get_run_logger()
        settings = get_settings()
        self.api_key = settings.news_api_key.get_secret_value()
        if not self.api_key:
            logger.error("News API key not found in settings")
            raise ValueError("News API key not found in settings.")
        logger.info("NewsApiFetcher initialized successfully")

    def _create_request_url(
        self, keywords: List[str], from_date: datetime, to_date: datetime
    ) -> str:
        """
        Create the request URL for the News API.

        Args:
            keywords (List[str]): A list of keywords to search for.
            from_date (datetime): The start date for the search.
            to_date (datetime): The end date for the search.

        Returns:
            str: The constructed request URL.
        """
        logger = get_run_logger()

        # Construct the base URL. To simplify we only get english articles
        # ordered by popularity. [TODO: set language and order mode as parameters]
        url = f"{self.BASE_URL}?apiKey={self.api_key}&language=en&sortBy=popularity"
        keyword_query = ""

        #  Dates should be in ISO 8601 format without UTC timezone and millisecond
        if from_date:
            url += f"&from={from_date.strftime('%Y-%m-%dT%H:%M:%S')}"
            logger.info(f"Added from_date filter: {from_date}")
        if to_date:
            url += f"&to={to_date.strftime('%Y-%m-%dT%H:%M:%S')}"
            logger.info(f"Added to_date filter: {to_date}")

        if len(keywords) > 0:
            # Ensure we don't exceed the maximum query length
            keyword_query = f"&q='{keywords[0]}'"
            for keyword in keywords[1:]:
                # Currently all keywords are treated as OR conditions
                # [TODO: investigate how to implement more complex conditions]
                tmp_query = keyword_query + f" OR '{keyword}'"
                if len(tmp_query) >= self.MAX_KEYWORDS_QUERY_CHARS:
                    logger.warning(
                        f"Keyword query truncated at {self.MAX_KEYWORDS_QUERY_CHARS} characters"
                    )
                    break
                keyword_query = tmp_query

        if len(keywords) > 0:
            url += keyword_query
            logger.info(f"Created request URL with {len(keywords)} keywords")
        else:
            logger.info("Created request URL without keyword filters")
        return url

    def _fetch_content(self, url: str) -> dict:
        """
        Fetch content from the News API.

        Args:
            url (str): The request URL for the News API.

        Returns:
            dict: The JSON response from the API or an error message.
        """
        
        logger = get_run_logger()
        logger.info("Fetching content from News API")
        response = requests.get(url)
        logger.info(f"Received response with status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            logger.info(
                f"Successfully fetched {data.get('totalResults', 0)} total results"
            )
            return data
        else:
            logger.error(
                f"Failed to fetch data from News API: {response.status_code} - {response.text}"
            )
            raise Exception(
                f"Failed to fetch data from News API: {response.status_code} - {response.text}"
            )

    def _get_content_size(self, content_head: str) -> int:
        """
        Get the size of the content of the article.

        News API only provides the 200 first characters of the content.
        If the content is truncated, the remaining size is added at the end.

        Args:
            content_head (str): The content head of the article.

        Returns:
            int: The estimated size of the full content.
        """
        
        size = len(content_head.encode("utf-8"))

        # News API adds at the end the full size as
        # ".. [+XXXX chars]"
        if content_head.endswith("]"):
            try:
                size += int(content_head.split("[+")[-1].split(" ")[0])
            except (ValueError, IndexError):
                pass
        return size

    def parse_articles(self, data: dict) -> List[ArticleEntry]:
        """
        Parse articles from the API response.

        Args:
            data (dict): The API response data.

        Returns:
            List[ArticleEntry]: A list of parsed articles.
        """
        logger = get_run_logger()
        articles = []
        raw_articles = data.get("articles", [])
        logger.info(f"Parsing {len(raw_articles)} articles from API response")

        for i, item in enumerate(raw_articles):
            logger.debug(f"Processing article {i + 1}/{len(raw_articles)}")

            # Convert ISO datetime to datetime object
            published_at_str = item.get("publishedAt", None)
            published_at = None
            if published_at_str:
                # The 'Z' indicates Zulu time i.e UTC+00:00
                published_at = datetime.fromisoformat(
                    published_at_str.replace("Z", "+00:00")
                )

            article = ArticleEntry(
                author=item.get("author") or "",
                title=item.get("title") or "",
                description=item.get("description") or "",
                url=item.get("url") or "",
                published_at=published_at,
                content_head=item.get("content") or "",
                content_size=self._get_content_size(item.get("content") or ""),
                source=item.get("source", {}).get("name") or "",
            )
            articles.append(article)

        if not articles:
            logger.error("No articles found in the response data")
            raise ValueError("No articles found in the response data.")

        logger.info(f"Successfully parsed {len(articles)} articles")
        return articles

    def fetch_data(
        self,
        keywords: List[str] = [],
        from_date: datetime = None,
        to_date: datetime = None,
    ) -> dict:
        """
        Fetch the articles from the News API.
        
        Args:
            keywords (List[str]): A list of keywords to search for.
            from_date (datetime, optional): The start date for the articles.
            to_date (datetime, optional): The end date for the articles.

        Returns:
            dict: The raw API response data.
        """
        
        
        logger = get_run_logger()
        logger.info(f"Starting data fetch with {len(keywords)} keywords")

        url = self._create_request_url(keywords, from_date, to_date)
        raw_data = self._fetch_content(url)
        logger.info("Data fetch completed successfully")
        return raw_data