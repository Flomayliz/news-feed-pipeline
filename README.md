# AI News Feed Pipeline

AI News Feed Pipeline is a modular and scalable application designed to fetch, process, and serve news articles based on specific topics. It leverages modern technologies like FastAPI, Prefect, MongoDB, and Docker to provide a robust and efficient solution for managing news data.

### How It Works

The system operates in two main components:

1. **Data Pipeline**:
   - **Fetch**: Retrieves raw news articles from NewsAPI based on configured topics and keywords.
   - **Process**: Filters out incomplete articles, removes irrelevant content, and classifies articles by topics.
   - **Store**: Saves the processed articles in MongoDB for efficient retrieval.

2. **Serving Layer**:
   - **API Service**: Provides RESTful endpoints to query the stored articles by topic, date range, etc.
   - **Web Interface**: A simple frontend that consumes the API to display news articles to users.

---

## Features

- **News Fetching**: Retrieves news articles from external APIs (e.g., NewsAPI).
- **Data Processing**: Cleans, filters, and enriches articles with topic classification.
- **Persistence**: Stores articles in MongoDB with efficient querying capabilities.
- **API**: Provides a RESTful API for accessing news articles and topics.
- **Web Interface**: Includes a simple frontend for browsing news articles.
- **Dockerized Deployment**: Supports containerized deployment for scalability.
- **Prefect Integration**: Orchestrates workflows for fetching, processing, and storing news.

---

## Prerequisites

- **Python**: Version `>=3.12`
- **Docker**: Installed and running
- **PDM**: Python Dependency Manager
- **MongoDB**: Running locally or in a container

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Flomayliz/news-feed-pipeline.git
   cd news-feed-pipeline
   ```

2. Make scripts executable:
   ```bash
   chmod +x scripts/*
   ```

3. Install dependencies:
   ```bash
   ./scripts/install_dependencies.sh
   ```

4. Install Docker (if not already installed):
   ```bash
   ./scripts/install_docker.sh
   ```

5. Install Python dependencies:
   ```bash
   pdm install
   ```

---

## Configuration

1. Copy the `.env.template` file to `.env`:
   ```bash
   cp .env.template .env
   ```

2. Update the `.env` file with your MongoDB URI and NewsAPI key:
   ```env
   MONGO_URI="mongodb://localhost:27017"
   MONGO_DB_NAME="ai_news_feed"
   NEWS_API_KEY="Your-NewsAPI-Key"
   ```

3. **Dynamic Configuration with Prefect Blocks**:
   
   The system automatically manages configuration through Prefect blocks:
   
   - **First Run**: When first started, the system automatically creates a configuration block based on your `.env` file (or defaults if not provided)
   - **Subsequent Runs**: Configuration is loaded from the Prefect block
   - **Updating Configuration**: You can modify parameters directly through the Prefect UI without changing code or restarting
   
   To update configuration through the UI:
   1. Access the Prefect dashboard at http://localhost:4200
   2. Navigate to "Blocks" section
   3. Edit the "NewsFeedConfig" block
   4. Save your changes (they will apply on the next flow run)

---

## Usage

### Local Testing

The following steps are for running and testing the application in a local environment:

1. Start MongoDB:
   ```bash
   pdm run start_mongo_server
   ```

2. Start Prefect Server:
   ```bash
   pdm run start_prefect_server
   ```

3. Start the News Pipeline:
   ```bash
   pdm run start_news_pipeline
   ```

4. Start the Web Server:
   ```bash
   pdm run start_web_server
   ```

### Access the Application

#### News Web Interface
- Access the web interface at: `http://localhost:8000`
- From here, you can:
  - View articles filtered by topic (AI, Marketing, Science)
  - Filter by date range
  - Adjust the number of articles displayed
  - Sort by relevance or date

<img src="docs/images/news_web_interface.gif" alt="News Web Interface" width="800" />

*News web interface showing topic filtering and article display*

#### API Documentation
- Access the FastAPI Swagger UI at: `http://localhost:8000/docs`
- Available endpoints:
  - `GET /api/get_topics`: Retrieve all available topics
  - `GET /api/get_news_by_topic`: Get news articles with filtering options

#### Prefect Dashboard
- Access the Prefect UI at: `http://localhost:4200`
- From the Prefect dashboard you can:
  - Monitor pipeline runs and their status
  - View logs and execution details
  - Manage workflow schedules
  - Track success/failure of each task in the pipeline

<img src="docs/images/prefect_dashboard.gif" alt="Prefect Dashboard" width="800" />

*Prefect dashboard showing pipeline execution with task status*

---

## Deployment

### Local Docker Deployment

1. Build the Docker image:
   ```bash
   docker compose -f docker/worker/docker-compose.yml build
   ```

2. Start the Prefect worker:
   ```bash
   prefect worker start --pool news-default-pool --type docker
   ```

3. Deploy the pipeline:
   ```bash
   python3 src/deploy.py
   ```

### Cloud Deployment

This application is designed to be cloud-ready thanks to its Prefect-based architecture. Prefect enables:

1. **Remote Workflow Orchestration**: Deploy and manage workflows in cloud environments.
2. **Scalable Execution**: Scale workers horizontally across cloud resources.
3. **Observability**: Monitor pipeline executions through Prefect Cloud UI.
4. **Failure Recovery**: Automatically handle failures and retries.

To deploy to the cloud:

1. Connect to Prefect Cloud:
   ```bash
   prefect cloud login
   ```

2. Create a work pool in Prefect Cloud:
   ```bash
   prefect work-pool create "cloud-pool" --type docker
   ```

3. Deploy the flow:
   ```bash
   python3 src/deploy.py --cloud --pool-name cloud-pool
   ```

4. Start a worker connected to your cloud account:
   ```bash
   prefect worker start --pool cloud-pool --type docker
   ```

This allows you to maintain local development workflows while also enabling robust cloud deployments when ready for production.

---

## Documentation

Detailed documentation about the project has been organized into separate files for better maintainability and clarity. All documentation can be accessed through our [Documentation Index](docs/index.md).

### Core Documentation

- [**System Architecture**](docs/architecture.md): Complete description of each component, data flow, and design decisions
- [**API Reference**](docs/api_reference.md): Comprehensive API documentation with endpoints and examples
- [**Advanced Configuration**](docs/advanced_configuration.md): Detailed configuration options and customization
- [**Future Improvements**](docs/future_improvements.md): Roadmap and planned enhancements

## high-level architecture

The high-level architecture diagram below shows how the different components interact:

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   News APIs   │────▶│  Prefect Flow  │────▶│   MongoDB    │
└───────────────┘     └───────────────┘     └───────────────┘
                             │                      │
                             │                      │
                             ▼                      ▼
                      ┌───────────────┐     ┌───────────────┐
                      │  FastAPI      │◀────│  Data Access  │
                      └───────────────┘     └───────────────┘
                             │
                             │
                             ▼
                      ┌───────────────┐
                      │  Web Frontend │
                      └───────────────┘
```

## Project Structure

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

---

## Dependencies

- **Python Libraries**:
  - `pandas`
  - `pydantic`
  - `requests`
  - `beautifulsoup4`
  - `prefect`
  - `motor`
  - `fastapi`
  - `uvicorn`
  - `pymongo`

- **Docker**:
  - MongoDB
  - Prefect Server

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Author

- **Leslie Ricardo de la Rosa**  
  Email: [leslie_ricardo@hotmail.com](mailto:leslie_ricardo@hotmail.com)

---

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## Configuration and Customization

The system is highly configurable to meet various needs. Basic configuration is done through the `.env` file as described above.

For detailed configuration options including topic management, API settings, and performance tuning, see the [Advanced Configuration Guide](docs/advanced_configuration.md).


## API Reference

The News Feed Pipeline offers a RESTful API for retrieving news articles and topics. For a complete reference including endpoints, parameters, and response examples, see the [API Reference Documentation](docs/api_reference.md).

Key endpoints include:
- `GET /api/get_topics`: Retrieve all available topics
- `GET /api/get_news_by_topic`: Get news articles with filtering options

The API can be explored interactively at `http://localhost:8000/docs` when the server is running.

## Development

This project welcomes contributions from developers. To get started with development:

1. Follow the [installation instructions](#installation) above
2. Review the [Development Guide](docs/development_guide.md) for detailed information on:
   - Adding new fetchers for additional news sources
   - Extending the topic classification system
   - Implementing new storage backends
   - Setting up testing and linting
   - Code style guidelines
   - Contributing workflow

The development guide includes code examples and best practices for extending the project functionality.

## Acknowledgments

- [NewsAPI](https://newsapi.org/) for providing news data.
- [Prefect](https://www.prefect.io/) for workflow orchestration.
- [FastAPI](https://fastapi.tiangolo.com/) for the API framework.


