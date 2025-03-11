import tomllib
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

toml_path = Path(__file__).parent.parent.parent / "player.toml"


class RaidSetting(BaseModel):
    url: str
    runs: int


class PlayerSetting(BaseSettings):
    raid: RaidSetting

    @classmethod
    def load_toml(cls, path: Path) -> "PlayerSetting":
        with open(path, "rb") as toml_file:
            player_data = tomllib.load(toml_file)
        return cls(**player_data)


player_setting = PlayerSetting.load_toml(toml_path)
