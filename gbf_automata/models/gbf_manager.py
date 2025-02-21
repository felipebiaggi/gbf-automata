import multiprocessing
from enum import Enum
from multiprocessing.managers import BaseManager


class RenderStatus(str, Enum):
    PENDING = "PENDING"
    RENDERING = "RENDERING"
    RENDERED = "RENDERED"
    ERROR = "ERROR"


class ConnectionStatus(str, Enum):
    DISCONNECTED = "DISCONNECTED"
    CONNECTED = "CONNECTED"


class StatusManager:
    def __init__(self):
        self.render_status = RenderStatus.PENDING
        self.render_condition = multiprocessing.Condition()
        self.connection_status = ConnectionStatus.DISCONNECTED
        self.connection_condition = multiprocessing.Condition()

    def set_render_status(self, new_render_status: RenderStatus) -> None:
        with self.render_condition:
            self.render_status = new_render_status
            self.render_condition.notify_all()

    def get_render_status(self) -> RenderStatus:
        return self.render_status

    def wait_for_render_status(self, expected_render_status) -> None:
        with self.render_condition:
            while self.render_status != expected_render_status:
                self.render_condition.wait()

            self.render_status = RenderStatus.PENDING

    def set_connection_status(self, new_connection_status: ConnectionStatus) -> None:
        with self.connection_condition:
            self.connection_status = new_connection_status
            self.connection_condition.notify_all()

    def get_connection_status(self) -> ConnectionStatus:
        return self.connection_status

    def wait_for_connection_status(self, expected_connection_status) -> None:
        with self.connection_condition:
            while self.connection_status != expected_connection_status:
                self.connection_condition.wait()

            self.connection_status = ConnectionStatus.DISCONNECTED


class GBFManager(BaseManager):
    pass


GBFManager.register("StatusManager", StatusManager)
