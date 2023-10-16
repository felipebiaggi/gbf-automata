from pydantic import BaseModel, Field
from gbf_automata.enums.arcarumv2_zone import ArcarumV2Zone


class SubZone(BaseModel):
    stage: int = Field(default=None, ge=1, le=3)
    node: int = Field(default=None, ge=1, le=7)


class Party(BaseModel):
    deck: int = Field(default=None, ge=1, le=7)
    group: int = Field(default=None, ge=1, le=6)


class ArcarumV2Model(BaseModel):
    zone: ArcarumV2Zone = Field(default=None)
    subzone: SubZone = Field(default=None)
    party: Party = Field(default=None)
