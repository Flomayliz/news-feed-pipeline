"""
Configuration settings for the application.
"""

from pydantic_settings import BaseSettings
from prefect.blocks.core import Block
from pydantic import BaseModel
from pydantic import SecretStr


class SystemConfiguration(BaseModel):
    """
    System configuration settings.
    This will use as the base for other configuration classes.
    """

    mongo_uri: str = ""
    news_api_key: SecretStr = ""
    mongo_db_name: str = "ai_news_feed"
    min_content_size: int = 1000
    min_title_size: int = 15
    score_threshold: int = 2
    get_full_text: bool = False


class LocalSettings(SystemConfiguration, BaseSettings):
    """
    Local configuration settings.
    These parameters are get from the environment variables.
    Check pydantic BaseSettings for more details

    BaseSettings and Block inherit from Pydantic's BaseModel.
    we just need to implement the required methods for Prefect blocks.
    """

    class Config:
        env_file = ".env"


class BlockSettings(SystemConfiguration, Block):
    """
    Prefect block configuration settings.

    Block and SystemConfiguration inherits from Pydantic's BaseModel.
    We just need to implement the required methods for Prefect blocks.
    """

    pass


def get_settings():
    """
    Get the application settings.

    This implementation follows a singleton pattern where
    the settings are loaded once and reused. It warranties that only
    one settings instance is created and used.
    """

    if not hasattr(get_settings, "settings"):
        try:
            get_settings.settings = BlockSettings.load("system-settings")
        except Exception:
            print("No block settings. Setting to default")
            get_settings.settings = LocalSettings()
            block_settings = BlockSettings(**get_settings.settings.model_dump())
            block_settings.save("system-settings", overwrite=True)

    return get_settings.settings
