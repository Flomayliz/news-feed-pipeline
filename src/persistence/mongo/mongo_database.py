"""
MongoDB implementation of the data persistence layer.
"""

from typing import List, Dict, Any
from pymongo import DESCENDING
from src.schemas import ArticleEntry
from datetime import datetime

from src.persistence.database import DataPersistence
from src.persistence.mongo.connection import (
    get_mongo_db,
    connect_to_mongo,
    get_mongo_client,
)


class MongoDataPersistence(DataPersistence):
    """
    MongoDB implementation of the data persistence layer.
    """
    
    def __init__(self):
        """Initialize MongoDB repository without establishing connection."""
        connect_to_mongo()
        self.client = get_mongo_client()
        self.db = get_mongo_db()
        self.collection = self.db["docs"]

    def _ensure_connection(self):
        """Ensure database connection is established."""
        if self.db is None:
            self.db = get_mongo_db()
            if self.db is None:
                raise RuntimeError(
                    "MongoDB connection not established. Call connect_to_mongo() first."
                )
            self.collection = self.db["docs"]

    def store_articles(self, articles: List[ArticleEntry]):
        self._ensure_connection()
        for article in articles:
            document = article.model_dump()
            # Use upsert to ensure uniqueness by URL
            self.collection.update_one(
                {"url": document["url"]},  # Filter by URL
                {"$set": document},        # Update/insert the document
                upsert=True               # Create if doesn't exist
            )

    def get_all_articles(self, order_by_date=True, limit=10) -> List[ArticleEntry]:
        self._ensure_connection()
        cursor = self.collection.find()
        if order_by_date:
            cursor = cursor.sort("published_at", DESCENDING)
        if limit > 0:
            cursor = cursor.limit(limit)

        articles = []
        for doc in list(cursor):
            articles.append(ArticleEntry(**doc))
        return articles

    def get_matching_articles(
        self,
        topics: List[str] = [],
        from_date: datetime = None,
        to_date: datetime = None,
        sort_by_match=False,
        limit=10,
    ) -> List[ArticleEntry]:
        self._ensure_connection()

        query: Dict[str, Any] = {}
        date_filter = {}
        if from_date:
            date_filter["$gte"] = from_date
        if to_date:
            date_filter["$lte"] = to_date
        if date_filter:
            query["published_at"] = date_filter

        # If topics is empty, always return all articles ordered by date, regardless of sort_by_match
        if not topics:
            cursor = self.collection.find(query)
            cursor = cursor.sort("published_at", DESCENDING)
            if limit > 0:
                cursor = cursor.limit(limit)
        elif sort_by_match:
            query["topics"] = {"$in": topics}
            pipeline = []
            if query:
                pipeline.append({"$match": query})

            pipeline.extend(
                [
                    {
                        "$addFields": {
                            "match_count": {
                                "$size": {"$setIntersection": ["$topics", topics]}
                            }
                        }
                    },
                    {"$sort": {"match_count": DESCENDING, "published_at": DESCENDING}},
                ]
            )

            if limit > 0:
                pipeline.append({"$limit": limit})

            cursor = self.collection.aggregate(pipeline)
        else:
            query["topics"] = {"$in": topics}
            cursor = self.collection.find(query)
            cursor = cursor.sort("published_at", DESCENDING)
            if limit > 0:
                cursor = cursor.limit(limit)

        articles = []
        for doc in list(cursor):
            articles.append(ArticleEntry(**doc))
        return articles