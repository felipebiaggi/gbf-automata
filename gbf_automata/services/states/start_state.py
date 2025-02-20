from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.data import get_data
from gbf_automata.services.states.base_state import State
from gbf_automata.util.scroll import scroll

data_model = get_data()


class StartState(State):
    def execute(self) -> GameStates:
        # move(element=data_model.main.home_bottom)

        # game_area = calibrate(self.machine.get_current_state())

        scroll(element=data_model.banner.arcarum)

        return GameStates.STOP
