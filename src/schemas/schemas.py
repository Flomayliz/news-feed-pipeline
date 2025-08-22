"""
DTO (Data Transfer Object) for article data.
"""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class ArticleEntry(BaseModel):
    """
    Data Transfer Object (DTO) for article data.
    Serves as common interfaces for the pipeline components.
    """
    author: str = Field("", description="Author of the article")
    title: str = Field("", description="Title of the article")
    description: str = Field("", description="Description of the article")
    url: str = Field("", description="URL of the article")
    published_at: datetime = Field(None, description="Publication date of the article")
    content_head: str = Field("", description="Content of the article")
    content_size: int = Field(0, description="Size of the article content in bytes")
    source: str = Field("", description="Source of the article, if available")
    topics: List[str] = Field(
        default_factory=list, description="List of topics associated with the article"
    )
