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


class BannerModel(BaseModel):
    arcarum: str
    gw: str


class ArcarumClassicModel(BaseModel):
    button: str


class ArcarumSandboxEletioModel(BaseModel):
    banner: str
    slithering_seductress: str


class ArcarumSandboxFaymModel(BaseModel):
    banner: str


class ArcarumSandboxGoliathModel(BaseModel):
    banner: str


class ArcarumSandboxHarbingerModel(BaseModel):
    banner: str


class ArcarumSandboxInvidiaModel(BaseModel):
    banner: str


class ArcarumSandboxJoculatorModel(BaseModel):
    banner: str


class ArcarumSandboxKalendaeModel(BaseModel):
    banner: str


class ArcarumSandboxLiberModel(BaseModel):
    banner: str


class ArcarumZonesModel(BaseModel):
    back_stage: str
    forward_stage: str
    eletio: ArcarumSandboxEletioModel
    faym: ArcarumSandboxFaymModel
    goliath: ArcarumSandboxGoliathModel
    harbinger: ArcarumSandboxHarbingerModel
    invidia: ArcarumSandboxInvidiaModel
    joculator: ArcarumSandboxJoculatorModel
    kalendae: ArcarumSandboxKalendaeModel
    liber: ArcarumSandboxLiberModel


class ArcarumSandboxModel(BaseModel):
    button: str
    zones: ArcarumZonesModel


class ArcarumModel(BaseModel):
    classic: ArcarumClassicModel
    sandbox: ArcarumSandboxModel


class RaidModel(BaseModel):
    ok: str
    attack: str


class DataModel(BaseModel):
    main: MainModel
    raid: RaidModel
    banner: BannerModel
    arcarum: ArcarumModel

    class Config:
        extra = "ignore"


@lru_cache()
def get_data() -> DataModel:
    with open("gbf_automata/data/images.json") as file:
        file_dict = json.load(file)  # dict

        return DataModel.model_validate(file_dict)
