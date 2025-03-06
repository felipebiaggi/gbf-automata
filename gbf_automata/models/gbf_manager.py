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


class CombatStatus(str, Enum):
    NOT_INITIATED = "NOT_INITIATED"
    STARTED = "STARTED"
    STOPPED = "STOPPED"
    ENDED = "ENDED"


class ResultStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"


class StatusManager:
    def __init__(self):
        self.render_status = RenderStatus.PENDING
        self.render_condition = multiprocessing.Condition()

        self.connection_status = ConnectionStatus.DISCONNECTED
        self.connection_condition = multiprocessing.Condition()

        self.combat_status = CombatStatus.NOT_INITIATED
        self.combat_condition = multiprocessing.Condition()

        self.result_status = ResultStatus.UNAVAILABLE
        self.result_condition = multiprocessing.Condition()

    def set_render_status(self, new_render_status: RenderStatus) -> None:
        with self.render_condition:
            self.render_status = new_render_status
            self.render_condition.notify_all()

    def get_render_status(self) -> RenderStatus:
        return self.render_status

    def wait_for_render_status(self, expected_render_status) -> None:
        self.render_status = RenderStatus.PENDING
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

    def set_combat_status(self, new_combat_status: CombatStatus) -> None:
        with self.combat_condition:
            self.combat_status = new_combat_status
            self.combat_condition.notify_all()

    def get_combat_status(self) -> CombatStatus:
        return self.combat_status

    def wait_for_combat_status(self, expected_combat_status) -> None:
        with self.combat_condition:
            while self.combat_status not in (
                expected_combat_status,
                CombatStatus.ENDED,
            ):
                self.combat_condition.wait()

    def set_result_status(self, new_result_status: ResultStatus) -> None:
        with self.result_condition:
            self.result_status = new_result_status
            self.result_condition.notify_all()

    def get_result_status(self) -> ResultStatus:
        return self.result_status

    def wait_for_result_status(self, expected_result_status) -> None:
        with self.result_condition:
            while self.result_status != expected_result_status:
                self.result_condition.wait()

        self.result_status = ResultStatus.UNAVAILABLE


class GBFManager(BaseManager):
    pass


GBFManager.register("StatusManager", StatusManager)
