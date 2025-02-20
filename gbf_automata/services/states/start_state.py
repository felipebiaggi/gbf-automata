from time import sleep

from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.data import get_data
from gbf_automata.models.render_manager import RenderStatus
from gbf_automata.services.states.base_state import State
from gbf_automata.util.move import move

data_model = get_data()


class StartState(State):
    def execute(self) -> GameStates:
        move(element=data_model.main.home_bottom)

        self.machine.render_status_manager.wait_for_status(RenderStatus.RENDERED)
        sleep(0.5)

        self.machine.receive_queue.put("arcarum")
        self.machine.render_status_manager.wait_for_status(RenderStatus.RENDERED)
        sleep(0.5)

        print("Terminou de renderizar o arcarum")

        # game_area = calibrate(self.machine.get_current_state())

        # scroll(element=data_model.banner.arcarum)

        return GameStates.STOP
