from time import sleep

from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.data import get_data
from gbf_automata.models.gbf_manager import ConnectionStatus, RenderStatus
from gbf_automata.services.states.base_state import State
from gbf_automata.util.calibration import calibrate

data_model = get_data()


class StartState(State):
    def execute(self) -> GameStates:
        self.machine.status_manager.wait_for_connection_status(
            ConnectionStatus.CONNECTED
        )

        self.machine.status_manager.wait_for_render_status(RenderStatus.RENDERED)
        sleep(1)

        self.machine.game_area = calibrate(self.machine.get_current_state())

        print("calibrou")

        return GameStates.RAID
