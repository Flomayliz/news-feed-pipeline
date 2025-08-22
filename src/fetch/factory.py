"""
News API fetcher factory.
"""

from src.fetch.fetcher import Fetcher
from src.fetch.fetchers.news_api_fetcher import NewsApiFetcher


def get_fetcher() -> Fetcher:
    """
    Get the news API fetcher.

    This function returns an instance of a Fetcher class depending on the configuration.
    It follows the factory design pattern although currently it only the NewsApiFetcher is
    implemented.
    [TODO: Implement other fetchers]
    """
    return NewsApiFetcher()
