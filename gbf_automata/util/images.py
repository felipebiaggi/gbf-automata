import json
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings

images_path = Path(__file__).parent.parent.parent / "images_path.json"


class MainModel(BaseModel):
    menu: str
    news: str
    home_top: str
    home_bottom: str
    back: str
    reload: str


class SupporterModel(BaseModel):
    ok: str


class RaidModel(BaseModel):
    attack: str
    next: str


class ResultModel(BaseModel):
    ok: str
    play_again: str


class Images(BaseSettings):
    main: MainModel
    supporter: SupporterModel
    raid: RaidModel
    result: ResultModel

    class Config:
        extra = "ignore"

    @classmethod
    def load_json(cls, path: Path) -> "Images":
        with open(path, "rb") as images_path_file:
            images_data = json.load(images_path_file)

        return cls(**images_data)


images = Images.load_json(images_path)
