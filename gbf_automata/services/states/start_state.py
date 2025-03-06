from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.data import get_data
from gbf_automata.models.gbf_manager import ConnectionStatus, RenderStatus
from gbf_automata.services.states.base_state import State
from gbf_automata.util import logger
from gbf_automata.util.logger import get_logger
from gbf_automata.util.move import move

data_model = get_data()

logger = get_logger()


class StartState(State):
    def execute(self) -> GameStates:
        logger.info("[State State] Execution")

        move(data_model.main.home_bottom)

        self.machine.status_manager.wait_for_connection_status(
            ConnectionStatus.CONNECTED
        )

        self.machine.status_manager.wait_for_render_status(RenderStatus.RENDERED)

        return GameStates.SUPPORTER
