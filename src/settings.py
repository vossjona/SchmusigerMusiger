from pathlib import Path
from typing import Self

from pydantic import BaseModel, ConfigDict, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from utils import read_file


class Settings(BaseSettings):
    """Contains settings for this project."""
    DISCORD_TOKEN: SecretStr = SecretStr("")

    BOT_CONFIGS_PATH: Path = Path("configs") / "config.yml"

    OPUS_LIB_NAME: str = "/opt/homebrew/Cellar/opus/1.5.2/lib/libopus.dylib"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_prefix="",
        extra="ignore",
    )


class BotConfig(BaseModel):
    prefix: str = "!"

    model_config = ConfigDict(protected_namespaces=())

    @classmethod
    def from_file(cls, filepath: Path) -> Self:
        """Use config json or yaml file to read bot configurations."""
        config = read_file(filepath)
        return cls.model_validate(config)
