import multiprocessing
from logging import exception

from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.game_area import GameArea
from gbf_automata.models.render_manager import RenderStatusManager
from gbf_automata.services.states.base_state import State
from gbf_automata.services.states.start_state import StartState


class StateMachine:
    def __init__(
        self,
        send_queue: multiprocessing.Queue,
        receive_queue: multiprocessing.Queue,
        render_status_manager: RenderStatusManager,
    ) -> None:
        self.render_status_manager: RenderStatusManager = render_status_manager
        self.send_queue: multiprocessing.Queue = send_queue
        self.receive_queue: multiprocessing.Queue = receive_queue
        self.states = {GameStates.START: StartState(self)}
        self.current_state: State = self.states[GameStates.START]

        self.game_area: GameArea

    def run(self) -> None:
        while True:
            next_state = self.current_state.execute()

            if next_state == GameStates.STOP:
                self.receive_queue.put("STOP")
                break

    def get_current_state(self) -> GameStates:
        for state_enum, state_class in self.states.items():
            if isinstance(self.current_state, type(state_class)):
                return state_enum
        raise exception()
