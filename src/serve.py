"""
Creates and serves the news pipeline locally.
"""

from src.flows.news_pipeline import news_pipeline_flow
from datetime import timedelta

if __name__ == "__main__":
    news_pipeline_flow.serve(
        name="local_pipeline",
        interval=timedelta(minutes=10),  # Run every 10 minutes
        description="Serves the news pipeline",
    )