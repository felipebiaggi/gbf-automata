from pydantic import BaseModel, Field
from gbf_automata.enums.arcarumv2_zone import ArcarumV2Zone

class Party(BaseModel):
    deck: int = Field(default=None, ge=1, le=7)
    group: int = Field(default=None, ge=1, le=6)


class ArcarumV2Model(BaseModel):
    zone: ArcarumV2Zone = Field(default=None)
    subzone: int = Field(default=None, ge=1, le=3)
    node: int = Field(default=None, ge=1, le=7)
    party: Party = Field(default=None)
