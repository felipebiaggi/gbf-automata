from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.gbf_manager import ConnectionStatus, RenderStatus
from gbf_automata.services.states.base_state import State
from gbf_automata.util.images import images
from gbf_automata.util.logger import get_logger
from gbf_automata.util.move import move

logger = get_logger()


class StartState(State):
    def execute(self) -> GameStates:
        logger.info("[START STATE] Execution")

        move(images.main.home_bottom)

        self.machine.status_manager.wait_for_connection_status(
            ConnectionStatus.CONNECTED
        )

        self.machine.status_manager.wait_for_render_status(RenderStatus.RENDERED)

        return GameStates.SUPPORTER
