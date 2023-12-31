import multiprocessing

from gbf_automata.enums.state import State
from gbf_automata.util.logger import get_logger


logger = get_logger(__name__)


class LoadState(object):
    def __init__(self) -> None:
        self._state: State = State.BLOCK
        self._lock = multiprocessing.Lock()

    def get_state(self) -> State:
        with self._lock:
            return self._state

    def set_state(self, value: State) -> None:
        with self._lock:
            if self._state != value:
                self._state = value
                logger.info(f"State change: <{self._state}>")
            else:
                logger.info(f"State doesn't change <{self._state}>")


def get_state() -> LoadState:
    return LoadState()
