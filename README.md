# ai-news-orchestrator


chmod +x scripts/*
./scripts/install_docker.sh
./scripts/install_dependencies.sh

pdm install

pdm run start_mongo_server
pdm run start_prefect_server
pdm run start_news_pipeline