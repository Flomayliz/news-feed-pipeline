"""
Base class for data persistence layer.
"""

from abc import ABC, abstractmethod
from src.schemas import ArticleEntry
from typing import List
from datetime import datetime


class DataPersistence(ABC):
    """
    Abstract base class for data persistence layer.
    """

    @abstractmethod
    def store_articles(self, articles: List[ArticleEntry]):
        """
        Store a list of articles in the persistence layer.

        Args:
            articles (List[ArticleEntry]): The list of articles to store.
        """
        pass

    @abstractmethod
    def get_all_articles(self, order_by_date=True, limit=10) -> List[ArticleEntry]:
        """
        Get all articles from the persistence layer.

        Args:
            order_by_date (bool): Whether to order articles by date.
            limit (int): The maximum number of articles to return.

        Returns:
            List[ArticleEntry]: The list of articles.
        """
        pass

    @abstractmethod
    def get_matching_articles(
        self,
        topics: List[str] = [],
        from_date: datetime = None,
        to_date: datetime = None,
        sort_by_match=False,
        limit=10,
    ) -> List[ArticleEntry]:
        """
        Get matching articles from the persistence layer.

        Args:
            topics (List[str]): The list of topics to match.
            from_date (datetime): The start date for the articles.
            to_date (datetime): The end date for the articles.
            sort_by_match (bool): Whether to sort articles by match relevance.
            limit (int): The maximum number of articles to return.

        Returns:
            List[ArticleEntry]: The list of matching articles.
        """
        pass
