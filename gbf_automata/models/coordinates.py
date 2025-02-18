import json
from functools import lru_cache
from typing import List

from pydantic import BaseModel

from gbf_automata.enums.arcarumv2_zone import ArcarumV2Zone


class CoordinateNodeModel(BaseModel):
    start: List[int]
    end: List[int]


class StageModel(BaseModel):
    stage: ArcarumV2Zone
    subzone: int
    node: int
    coordinate: CoordinateNodeModel


class CoordinateModel(BaseModel):
    stages: List[StageModel]

    class Config:
        extra = "ignore"


@lru_cache()
def get_coordinates() -> CoordinateModel:
    with open("src/gbf_automata/data/arcarum_v2/coordinates.json") as file:
        file_dict = json.load(file)

        return CoordinateModel.model_validate(file_dict)


coordinates = get_coordinates()
