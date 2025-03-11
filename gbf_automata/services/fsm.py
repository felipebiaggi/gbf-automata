import multiprocessing

from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.game_area import GameArea
from gbf_automata.models.gbf_manager import StatusManager
from gbf_automata.models.message import Message, MessageAction, MessageType
from gbf_automata.services.states.base_state import State
from gbf_automata.services.states.raid_state import RaidState
from gbf_automata.services.states.result_state import ResultState
from gbf_automata.services.states.start_state import StartState
from gbf_automata.services.states.supporter_state import SupporterState
from gbf_automata.util.logger import get_logger

logger = get_logger()

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
            GameStates.SUPPORTER: SupporterState(self),
            GameStates.RAID: RaidState(self),
            GameStates.RESULT: ResultState(self),
        }
        self.current_state: State = self.states[GameStates.START]

        self.game_area: GameArea

        self.runs = 1

    def run(self) -> None:
        try:
            logger.info("[STATE MACHINE] Startup")
            while True:
                next_state = self.current_state.execute()

                logger.info(f"[STATE MACHINE] State Trasition: {next_state}")

                if next_state == GameStates.SUPPORTER:
                    self.current_state = self.states[next_state]

                if next_state == GameStates.RAID:
                    self.current_state = self.states[next_state]

                if next_state == GameStates.RESULT:
                    self.current_state = self.states[next_state]

                if next_state == GameStates.STOP:
                    self.message_queue.put(stop_message)
                    break
        except Exception as e:
            logger.warning(f"[STATE MACHINE] Error: {e}")
            self.message_queue.put(stop_message)
