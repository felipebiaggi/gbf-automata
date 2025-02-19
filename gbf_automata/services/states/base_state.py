from __future__ import annotations

from abc import ABC, abstractmethod

from gbf_automata.enums.game_states import GameStates


class State(ABC):
    def __init__(self, machine: "StateMachine"):
        self.machine: "StateMachine" = machine

    @abstractmethod
    def execute(self) -> GameStates: ...
