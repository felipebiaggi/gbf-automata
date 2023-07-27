from pydantic import BaseModel


class Display(BaseModel):
    left: int
    top: int
    width: int
    height: int
