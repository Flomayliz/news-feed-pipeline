"""
Factory functions for creating persistence layer components.
"""

from src.persistence.database import DataPersistence
from src.persistence.mongo.mongo_database import MongoDataPersistence


def get_database() -> DataPersistence:
    """
    Create a database instance for the persistence layer.

    This function returns an instance of a DataPersistence class depending on the configuration.
    It follows the factory design pattern although currently it only the MongoDataPersistence is
    implemented.
    [TODO: Implement other DataPersistence implementations]

    Returns:
        DataPersistence: The database instance.
    """

    return MongoDataPersistence()
