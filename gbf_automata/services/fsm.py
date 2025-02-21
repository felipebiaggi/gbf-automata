import multiprocessing
from logging import exception

from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.game_area import GameArea
from gbf_automata.models.gbf_manager import StatusManager
from gbf_automata.models.message import Message, MessageAction, MessageType
from gbf_automata.services.states.base_state import State
from gbf_automata.services.states.raid_state import RaidState
from gbf_automata.services.states.start_state import StartState

stop_message = Message(
    message_type=MessageType.INTERNAL,
    message_action=MessageAction.STOP,
)


class StateMachine:
    def __init__(
        self,
        message_queue: multiprocessing.Queue,
        status_manager: StatusManager,
    ) -> None:
        self.status_manager: StatusManager = status_manager
        self.message_queue: multiprocessing.Queue = message_queue
        self.states = {
            GameStates.START: StartState(self),
            GameStates.RAID: RaidState(self),
        }
        self.current_state: State = self.states[GameStates.START]

        self.game_area: GameArea

    def run(self) -> None:
        try:
            while True:
                next_state = self.current_state.execute()

                if next_state == GameStates.RAID:
                    self.current_state = self.states[next_state]

                if next_state == GameStates.STOP:
                    self.message_queue.put(stop_message)
                    break
        except Exception as e:
            print(f"Error {e}")
            self.message_queue.put(stop_message)

    def get_current_state(self) -> GameStates:
        for state_enum, state_class in self.states.items():
            if isinstance(self.current_state, type(state_class)):
                return state_enum
        raise exception()
