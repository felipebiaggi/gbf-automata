import multiprocessing
from enum import Enum
from multiprocessing.managers import BaseManager


class RenderStatus(str, Enum):
    PENDING = "PENDING"
    RENDERING = "RENDERING"
    RENDERED = "RENDERED"
    ERROR = "ERROR"


class RenderStatusManager:
    def __init__(self):
        self.status = RenderStatus.PENDING
        self.condition = multiprocessing.Condition()

    def set_status(self, new_status: RenderStatus) -> None:
        with self.condition:
            self.status = new_status
            self.condition.notify_all()

    def get_status(self) -> RenderStatus:
        return self.status

    def wait_for_status(self, expected_status) -> None:
        with self.condition:
            while self.status != expected_status:
                self.condition.wait()

            self.status = RenderStatus.PENDING


class RenderManager(BaseManager):
    pass


RenderManager.register("RenderStatusManager", RenderStatusManager)
