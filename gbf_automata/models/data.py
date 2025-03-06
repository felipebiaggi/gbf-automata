import json
from functools import lru_cache

from pydantic import BaseModel


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


class DataModel(BaseModel):
    main: MainModel
    supporter: SupporterModel
    raid: RaidModel
    result: ResultModel

    class Config:
        extra = "ignore"


@lru_cache()
def get_data() -> DataModel:
    with open("gbf_automata/data/images.json") as file:
        file_dict = json.load(file)  # dict

        return DataModel.model_validate(file_dict)
