from gbf_automata.schema.display import Display
from gbf_automata.schema.image_area import ImageModel
from typing import List


class GameArea:
    def __init__(
        self,
        display_identify: int,
        aspect_ratio: dict,
        menu: ImageModel,
        news: ImageModel,
        home: ImageModel,
        back: ImageModel,
        reload: ImageModel
    ) -> None:
        self._display_identify = display_identify
        self._aspect_ratio = Display(**aspect_ratio)
        self._menu: ImageModel = menu
        self._news: ImageModel = news
        self._home: ImageModel = home
        self._back: ImageModel = back
        self._reload: ImageModel = reload

    def __repr__(self) -> str:
        return (
            f"Display ID {self._display_identify} "
            f"Aspect Ratio {self._aspect_ratio} "
        )

    def accuracy(self) -> List[float]:
        return [self._menu.accuracy(), self._news.accuracy(), self._home.accuracy(), self._back.accuracy(), self._reload.accuracy()]

        ### Display ###

    ##########################################################################
    #
    #                    (Game Area)
    #  (top, left) -> +--------------+
    #                 |              |
    #                 |              |
    #                 |              |
    #                 |              |
    #                 |              |
    #                 |              |
    #                 |              |
    #                 |              |
    #                 +--------------+
    #
    #
    #

    def area(self) -> dict:
        return {
            "top": self._aspect_ratio.top + self._news.min_loc[1],
            "left": self._aspect_ratio.left + self._news.min_loc[0],
            "width": self._aspect_ratio.width
            - (
                self._aspect_ratio.width
                - (self._menu.min_loc[0] + self._menu.image_width)
            )
            - self._news.min_loc[0],
            "height": self._aspect_ratio.height
            - (
                self._aspect_ratio.height
                - (self._home.min_loc[1] + self._home.image_height)
            )
            - self._news.min_loc[1],
            "mon": self._display_identify,
        }

    def full_area(self) -> dict:
        return {
            "top": self._aspect_ratio.top,
            "left": self._aspect_ratio.left,
            "width": self._aspect_ratio.width,
            "height": self._aspect_ratio.height,
            "mon": self._display_identify,
        }
