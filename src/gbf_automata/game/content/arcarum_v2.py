from __future__ import annotations
import typing

from gbf_automata.util.settings import settings


if typing.TYPE_CHECKING:
    from gbf_automata.game.gbf import GBFGame


class ArcarumV2:
    def __init__(
        self,
        game: GBFGame
    ):
        self.game: GBFGame = game
    


    def start(self):
        arcarum = None

        for _ in range(0, self.game.max_attemps):
            result = self.game.search_for_element(
                element=settings
            )

