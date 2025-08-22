from prefect.docker import DockerImage
from prefect import flow

if __name__ == "__main__":
    flow.from_source(
        "https://github.com/Flomayliz/news-feed-pipeline.git",
        entrypoint="src/flows/news_pipeline.py:news_pipeline_flow",
    ).deploy(
        name="news_pipeline_local",
        work_pool_name="news-default-pool",
        job_variables={"image_pull_policy": "Never"},
        image="news_pipeline_image:latest",
        build=False,
        push=False,
    )
