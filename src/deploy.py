from src.flows.news_pipeline import news_pipeline_flow
from prefect.docker import DockerImage
from prefect import flow


if __name__ == "__main__":
    news_pipeline_flow.deploy(
        name="news_pipeline_local",
        work_pool_name="news-default-pool",
        image=DockerImage(
            name="news_pipeline_image",
            tag="latest",
            dockerfile="../docker/worker_image/Dockerfile",
        ),
        push=False,
    )
