"""
MongoDB connection management.

This module provides functions for establishing and closing MongoDB connections.
"""

from pymongo import MongoClient
from src.core.config import get_settings, LocalSettings

# Global variables to store database connection
_client = None
_db = None


def connect_to_mongo():
    """
    Initialize connection to MongoDB.

    This function should be called at the start of the application
    to establish the database connection.
    """
    global _client, _db

    settings = get_settings()
    
    # Handle settings if it's a coroutine (for testing purposes)
    if hasattr(settings, "__await__"):
        import asyncio
        try:
            settings = asyncio.run(settings)
        except RuntimeError:  # If inside another event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                print("Warning: Using synchronous fallback for async settings")
                settings = LocalSettings()  # Fallback to local settings
            else:
                settings = loop.run_until_complete(settings)

    # Create client if it doesn't exist
    if _client is None:
        _client = MongoClient(settings.mongo_uri)
        _db = _client[settings.mongo_db_name]


def close_mongo_connection():
    """
    Close the MongoDB connection.

    This function should be called when shutting down the application
    to ensure proper cleanup of database resources.
    """
    global _client, _db

    if _client is not None:
        _client.close()
        _client = None
        _db = None


def get_mongo_client():
    """
    Get the current MongoDB client.

    Returns:
        The current MongoClient instance or None if not connected
    """
    return _client


def get_mongo_db():
    """
    Get the current MongoDB database.

    Returns:
        The current MongoDB database instance or None if not connected
    """
    return _db
