from time import sleep

from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.data import get_data
from gbf_automata.models.gbf_manager import CombatStatus, RenderStatus
from gbf_automata.models.message import Message, MessageAction, MessageType
from gbf_automata.services.states.base_state import State
from gbf_automata.util.move import move

data_model = get_data()


class RaidState(State):
    def execute(self) -> GameStates:
        self.machine.message_queue.put(
            Message(
                message_type=MessageType.EXTERNAL,
                message_action=MessageAction.MOVE,
                extra="https://game.granbluefantasy.jp/#replicard/supporter/10/10/6/819161/25",
            )
        )

        self.machine.status_manager.wait_for_render_status(RenderStatus.RENDERED)
        sleep(1)

        move(data_model.raid.ok)

        while True:
            self.machine.status_manager.wait_for_combat_status(CombatStatus.STOPPED)
            sleep(1)

            move(element=data_model.raid.attack)
        return GameStates.STOP
