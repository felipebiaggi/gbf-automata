from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.data import get_data
from gbf_automata.models.gbf_manager import RenderStatus
from gbf_automata.services.states.base_state import State

data_model = get_data()


class ResultState(State):
    def execute(self) -> GameStates:
        print(self.machine.status_manager.get_render_status())
        self.machine.status_manager.wait_for_render_status(RenderStatus.RENDERED)
        print("render finished")

        return GameStates.STOP
