import multiprocessing
from gbf_automata.enums.state import State


class GameState(object):
    def __init__(self) -> None:
        self._state: State
        self._lock = multiprocessing.Lock()

    @property
    def state(self) -> State:
        with self._lock:
            return self._state

    @state.setter
    def state(self, value: State) -> None:
        with self._lock:
            self._state = value


def get_state() -> State:
    return State()
