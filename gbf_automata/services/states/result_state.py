from time import sleep

from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.data import get_data
from gbf_automata.models.gbf_manager import ResultStatus
from gbf_automata.services.states.base_state import State
from gbf_automata.util.move import move

data_model = get_data()


class ResultState(State):
    def execute(self) -> GameStates:
        self.machine.status_manager.wait_for_result_status(ResultStatus.AVAILABLE)
        sleep(1)

        print("move para ok")
        move(data_model.result.ok)
        sleep(1)

        return GameStates.SUPPORTER
