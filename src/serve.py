"""
Creates and serves the news pipeline locally.
"""

from datetime import timedelta
from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        ".",
        entrypoint="src/flows/news_pipeline.py:news_pipeline_flow",
    ).serve(
        name="local_pipeline",
        interval=timedelta(minutes=10),  # Run every 10 minutes
        description="Serves the news pipeline",
    )