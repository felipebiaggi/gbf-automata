from __future__ import annotations
import typing

import pyautogui
from gbf_automata.enums.arcarumv2_zone import ArcarumV2Zone
from gbf_automata.exception.gbf_automata_exception import GBFAutomataError

from gbf_automata.util.settings import settings
from gbf_automata.schema.data import data_model


if typing.TYPE_CHECKING:
    from gbf_automata.game.gbf import GBFGame


class ArcarumV2:
    def __init__(self, game: GBFGame):
        self.game: GBFGame = game

    def reset_zone(self) -> None:
        back_button = self.game.search_for_element(
            element=data_model.arcarum.sandbox.zones.back_stage
        )
 
        pyautogui.moveTo(*back_button.center())
        pyautogui.click()
        self.game.wait()
        pyautogui.click()

    def zone(self, element: str) -> None:
        zone = self.game.search_for_element(element=element)
   
        pyautogui.moveTo(*zone.center())

        pyautogui.click()

        self.game.wait()
    

    def select_node(self) -> None:
        pass
        
    def start(self) -> None:
        # SEARCH FOR ARCARUM BANNER
        self.game.search_for_element_and_scroll(
            element=data_model.banner.arcarum, accuracy_threshold=0.80
        )

        # CHECK THE ARCARUM TYPE
        try:
            self.game.search_for_element(
                element=data_model.arcarum.sandbox.button
            )
        except GBFAutomataError:
            arcarum_sandbox = self.game.search_for_element(
                element=data_model.arcarum.classic.button
            )

            pyautogui.moveTo(*arcarum_sandbox.center())

            pyautogui.click()

            self.game.wait()

        # SELECT THE ARCARUM ZONE
        if ArcarumV2Zone.ELETIO == settings.arcarum_v2.zone:
            self.zone(element=data_model.arcarum.sandbox.zones.eletio.banner)

            self.reset_zone()
