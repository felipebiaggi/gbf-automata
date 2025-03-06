from time import sleep

from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.data import get_data
from gbf_automata.models.gbf_manager import CombatStatus
from gbf_automata.services.states.base_state import State
from gbf_automata.util.move import move

data_model = get_data()


class RaidState(State):
    def execute(self) -> GameStates:
        turn = 1

        while True:
            self.machine.status_manager.wait_for_combat_status(CombatStatus.STOPPED)
            sleep(1)

            if self.machine.status_manager.get_combat_status() == CombatStatus.ENDED:
                move(data_model.raid.next)
                self.machine.status_manager.set_combat_status(
                    CombatStatus.NOT_INITIATED
                )
                return GameStates.RESULT

            move(element=data_model.raid.attack)

            print(f"Turn: <{turn}>")

            turn += 1

        return GameStates.STOP
