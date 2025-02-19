from gbf_automata.enums.game_states import GameStates
from gbf_automata.services.states.base_state import State
from gbf_automata.util.calibration import calibrate


class StartState(State):
    def execute(self) -> GameStates:
        game_area = calibrate(self.machine.get_current_state())

        print(game_area.area())
        return GameStates.STOP
