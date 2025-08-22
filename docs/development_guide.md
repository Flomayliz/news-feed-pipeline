# Development Guide

This guide provides information for developers who want to extend or modify the News Feed Pipeline.

## Project Structure

The project follows a modular architecture, with clear separation of concerns:

- **`src/`**: Contains the main application code.
  - **`api/`**: FastAPI application for serving the API and frontend.
  - **`core/`**: Core utilities like configuration and topic management.
  - **`fetch/`**: Fetchers for retrieving news articles.
  - **`flows/`**: Prefect workflows for orchestrating the pipeline.
  - **`persistence/`**: MongoDB integration for data storage.
  - **`process/`**: Data processing and enrichment logic.
  - **`schemas/`**: Pydantic models for data validation.

- **`docker/`**: Docker configurations for MongoDB, Prefect, and workers.
- **`scripts/`**: Helper scripts for installation and setup.

## Development Setup

1. Follow the [installation instructions](../README.md#installation) in the main README.
2. Set up a development environment:
   ```bash
   pdm install --dev
   ```
3. Configure pre-commit hooks (optional but recommended):
   ```bash
   pre-commit install
   ```

## Adding a New Fetcher

To add support for a new news source:

1. Create a new class in `src/fetch/fetchers/` that implements the `Fetcher` interface:
   ```python
   from src.fetch.fetcher import Fetcher
   
   class MyNewFetcher(Fetcher):
       """Fetcher implementation for MyNewSource API."""
       
       def fetch_articles(self, keywords: list[str], from_date: str, to_date: str) -> list[dict]:
           """Fetch articles from MyNewSource API."""
           # Implementation goes here
           pass
   ```

2. Update the `get_fetcher` factory function in `src/fetch/factory.py`:
   ```python
   def get_fetcher() -> Fetcher:
       """Get the configured fetcher instance."""
       fetcher_type = os.getenv("FETCHER_TYPE", "news_api").lower()
       
       if fetcher_type == "news_api":
           return NewsApiFetcher()
       elif fetcher_type == "my_new_source":
           return MyNewFetcher()
       else:
           raise ValueError(f"Unsupported fetcher type: {fetcher_type}")
   ```

3. Add any required configuration parameters to `.env.template`:
   ```
   # MyNewSource API configuration
   MY_NEW_SOURCE_API_KEY=your_api_key_here
   ```

## Extending the Topic System

The topic classification system uses a simple keyword-based approach defined in `src/core/topic_dictionary.py`.

### Adding New Topics

1. Modify `src/core/topic_dictionary.py` to add new topics or keywords:
   ```python
   TOPIC_KEYWORDS = {
       # Existing topics...
       "technology": [
           "tech",
           "gadget",
           "smartphone",
           "software",
           # Add more keywords...
       ],
   }
   ```

2. To modify the classification logic, update `src/process/process_data.py`:
   ```python
   def classify_article_by_topics(article: ArticleEntry) -> list[str]:
       """Classify an article by topics based on its content."""
       # Your custom classification logic here
       pass
   ```

### Topic Classification Tuning

- Adjust the `SCORE_THRESHOLD` in the `.env` file to control the sensitivity of topic classification
- Higher threshold = fewer topics assigned (more specific)
- Lower threshold = more topics assigned (more inclusive)

## Adding a New Storage Backend

To implement a new database backend:

1. Create a new class that implements the `DataPersistence` interface:
   ```python
   from src.persistence.database import DataPersistence
   
   class MyNewDatabasePersistence(DataPersistence):
       """Implementation for a new database backend."""
       
       def save_articles(self, articles: list[ArticleEntry]) -> None:
           """Save articles to the database."""
           # Implementation goes here
           pass
           
       def get_news_by_topic(self, topics: list[str] = None, limit: int = 10,
                          from_date: datetime = None, to_date: datetime = None,
                          sort_by_match: bool = False) -> list[ArticleEntry]:
           """Get news articles filtered by topic."""
           # Implementation goes here
           pass
   ```

2. Update the factory in `src/persistence/factory.py`

## Code Style and Linting

The project follows strict style guidelines and uses [Ruff](https://github.com/charliermarsh/ruff) as an all-in-one Python linter and formatter. Ruff is already configured in the project's `pyproject.toml` file and included as a development dependency.

### Ruff Features

- Code formatting with consistent style rules
- Import sorting and organization
- Comprehensive linting and error checking
- Automated code quality enforcement

### Using Ruff

The project includes pre-configured PDM scripts for code quality:

```bash
# Install development dependencies including Ruff
pdm install -G lint

# Check code for style issues without modifying
pdm run lint

# Format code in-place
pdm run format

# Check and fix auto-fixable issues
pdm run ruff check --fix .
```

## Documentation

When extending the project, please update the documentation:

1. Update relevant markdown files in the `docs/` directory
2. Add new files for major features or components
3. Update the [Documentation Index](index.md) with links to new documentation

## Prefect Integration

When modifying the workflow:

1. Update the flow definition in `src/flows/news_pipeline.py`
2. Test locally with `pdm run start_news_pipeline`
3. Re-deploy with `python src/deploy.py`
