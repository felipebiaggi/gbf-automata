from pydantic import BaseModel


class DisplayModel(BaseModel):
    left: int
    top: int
    width: int
    height: int
