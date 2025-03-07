from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.data import get_data
from gbf_automata.models.gbf_manager import ResultStatus
from gbf_automata.services.states.base_state import State
from gbf_automata.util.delay import random_delay
from gbf_automata.util.logger import get_logger

data_model = get_data()

logger = get_logger()


class ResultState(State):
    def execute(self) -> GameStates:
        logger.info("[RESULT STATE] Execution")
        self.machine.status_manager.wait_for_result_status(ResultStatus.AVAILABLE)
        random_delay()

        # move(data_model.result.ok)
        # random_delay()

        return GameStates.SUPPORTER
