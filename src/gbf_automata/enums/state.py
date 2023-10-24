from enum import Enum


class State(str, Enum):
    NONE = "NONE"
    DONE = "DONE"
    LOADING = "LOADING"
