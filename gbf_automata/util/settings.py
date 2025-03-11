import tomllib
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

toml_path = Path(__file__).parent.parent.parent / "settings.toml"


class RaidSetting(BaseModel):
    url: str
    runs: int


class ServerSetting(BaseModel):
    host: str
    port: str


class LogSettings(BaseModel):
    level: str
    format: str


class Settings(BaseSettings):
    raid: RaidSetting
    log: LogSettings
    server: ServerSetting

    @classmethod
    def load_toml(cls, path: Path) -> "Settings":
        with open(path, "rb") as toml_file:
            player_data = tomllib.load(toml_file)
        return cls(**player_data)


settings = Settings.load_toml(toml_path)
