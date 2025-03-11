from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.data import get_data
from gbf_automata.models.gbf_manager import RenderStatus
from gbf_automata.models.message import Message, MessageAction, MessageType
from gbf_automata.services.states.base_state import State
from gbf_automata.util.delay import random_delay
from gbf_automata.util.logger import get_logger
from gbf_automata.util.move import move
from gbf_automata.util.player_settings import player_setting

data_model = get_data()

logger = get_logger()


class SupporterState(State):
    def execute(self) -> GameStates:
        logger.info("[SUPPORTER STATE] Execution")
        if self.machine.runs <= player_setting.raid.runs:
            logger.info(f"[SUPPORTER STATE] Starting run {self.machine.runs}")

            self.machine.message_queue.put(
                Message(
                    message_type=MessageType.EXTERNAL,
                    message_action=MessageAction.MOVE,
                    extra=player_setting.raid.url,
                )
            )

            self.machine.status_manager.wait_for_render_status(RenderStatus.RENDERED)
            random_delay()

            move(data_model.supporter.ok)

            return GameStates.RAID

        return GameStates.STOP
