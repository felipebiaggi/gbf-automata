from gbf_automata.enums.game_states import GameStates
from gbf_automata.models.gbf_manager import CombatStatus
from gbf_automata.services.states.base_state import State
from gbf_automata.util.delay import random_delay
from gbf_automata.util.images import images
from gbf_automata.util.logger import get_logger
from gbf_automata.util.move import move

logger = get_logger()


class RaidState(State):
    def execute(self) -> GameStates:
        logger.info("[RAID STATE] Execution")
        turn = 1

        while True:
            self.machine.status_manager.wait_for_combat_status(CombatStatus.STOPPED)
            random_delay()

            if self.machine.status_manager.get_combat_status() == CombatStatus.ENDED:
                move(images.raid.next)
                self.machine.status_manager.set_combat_status(
                    CombatStatus.NOT_INITIATED
                )
                return GameStates.RESULT

            move(element=images.raid.attack)

            logger.info(f"[RAID STATE] Turn: {turn}")

            turn += 1

        return GameStates.STOP
