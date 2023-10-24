import multiprocessing
from gbf_automata.enums.state import State


class LoadState(object):
    def __init__(self) -> None:
        self._state = State.NONE
        self._lock = multiprocessing.Lock()

    @property
    def state(self):
        with self._lock:
            return self._state

    @state.setter
    def state(self, value):
        with self._lock:
            self._state = value

    @state.getter
    def state(self):
        with self._lock:
            return self._state
