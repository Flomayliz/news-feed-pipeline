"""
Base class for all fetchers.
"""

from src.schemas import ArticleEntry
from typing import List
from datetime import datetime
from abc import ABC, abstractmethod


class Fetcher(ABC):
    """
    Abstract base class for all fetchers.

    Defines an interface for fetching articles from various sources.
    """

    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def fetch_data(
        self,
        keywords: List[str] = [],
        from_date: datetime = None,
        to_date: datetime = None,
    ) -> dict:
        """
        Fetch data from the source.

        Args:
            keywords (List[str], optional): List of keywords to filter articles.
            from_date (datetime, optional): Start date for fetching articles.
            to_date (datetime, optional): End date for fetching articles.

        Returns:
            dict: The raw fetched data.

        """
        pass

    @abstractmethod
    def parse_articles(self, article_data: dict) -> List[ArticleEntry]:
        """
        Parse the article data into a list of ArticleEntry objects.

        Args:
            article_data (dict): The raw article data.

        Returns:
            List[ArticleEntry]: A list of parsed ArticleEntry objects.

        """
        pass
