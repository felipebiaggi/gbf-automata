from __future__ import annotations
import typing

import pyautogui
from gbf_automata.enums.arcarumv2_zone import ArcarumV2Zone
from gbf_automata.exception.gbf_automata_exception import GBFAutomataError

from gbf_automata.util.settings import settings


if typing.TYPE_CHECKING:
    from gbf_automata.game.gbf import GBFGame


class ArcarumV2:
    def __init__(self, game: GBFGame):
        self.game: GBFGame = game

    def reset_zone(self):
        back_buttom = self.game.search_for_element(element=settings.image_back_stage)

        pyautogui.moveTo(*back_buttom.center())
        pyautogui.click()
        self.game.wait()
        pyautogui.click()

    def zone(self, element: str):
        zone = self.game.search_for_element(element=element)

        if zone.accuracy() < self.game.accuracy_threshold:
            raise GBFAutomataError("Arcarum Zone not found!")

        pyautogui.moveTo(*zone.center())

        pyautogui.click()

        self.game.wait(4.0)

    def start(self):
        # SEARCH FOR ARCARUM BANNER
        self.game.search_for_element_and_scroll(element=settings.image_arcarum)

        # CHECK THE ARCARUM TYPE
        type_arcarum = self.game.search_for_element(
            element=settings.image_button_classic
        )

        if type_arcarum.accuracy() < self.game.accuracy_threshold:
            arcarum_sandbox = self.game.search_for_element(
                element=settings.image_button_sandbox
            )

            if arcarum_sandbox.accuracy() < self.game.accuracy_threshold:
                raise GBFAutomataError("Invalid Page")

            pyautogui.moveTo(*arcarum_sandbox.center())

            pyautogui.click()

            self.game.wait(4.0)

        # SELECT THE ARCARUM ZONE
        if ArcarumV2Zone.ELETIO == settings.arcarum_v2.zone:
            self.zone(element=settings.image_zone_eletio)

            self.reset_zone()
