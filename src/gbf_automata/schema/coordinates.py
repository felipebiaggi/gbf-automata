import json
from typing import List, Any, Dict
from pydantic import Field, BaseModel

class NodeModel(BaseModel):
    node: Dict[Any, Any]

class SubStageModel(BaseModel):
    one: NodeModel = Field(..., alias="1")
    # two: NodeModel = Field(..., alias="2")
    # three: NodeModel = Field(..., alias="3")


class StageModel(BaseModel):
    substage: SubStageModel


class CoordinateModel(BaseModel):
    eletio: StageModel
    
    class Config:
        extra = "ignore"


if __name__ == "__main__":
    with open("src/gbf_automata/data/arcarum_v2/test.json") as file:
        file_dict = json.load(file)

        model = CoordinateModel.model_validate(file_dict)

        print(model.eletio.substage.one)

