from gbf_automata.schema.display import Display
from gbf_automata.schema.image_area import ImageModel
from typing import List, Tuple


class GameArea:
    def __init__(
        self,
        display_identify: int,
        aspect_ratio: dict,
        menu: ImageModel,
        news: ImageModel,
        home: ImageModel,
        back: ImageModel,
        reload: ImageModel,
    ) -> None:
        self.display_identify = display_identify
        self.aspect_ratio = Display(**aspect_ratio)
        self.menu: ImageModel = menu
        self.news: ImageModel = news
        self.home: ImageModel = home
        self.back: ImageModel = back
        self.reload: ImageModel = reload

    def __repr__(self) -> str:
        return (
            f"Display ID {self.display_identify} "
            f"Aspect Ratio {self.aspect_ratio} "
        )

    def accuracy(self) -> List[float]:
        return [
            self.home.accuracy(),
        ]

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
            "top": self.aspect_ratio.top + self.news.min_loc[1],
            "left": self.aspect_ratio.left + self.news.min_loc[0],
            "width": self.aspect_ratio.width
            - (
                self.aspect_ratio.width
                - (self.menu.min_loc[0] + self.menu.image_width)
            )
            - self.news.min_loc[0],
            "height": self.aspect_ratio.height
            - (
                self.aspect_ratio.height
                - (self.home.min_loc[1] + self.home.image_height)
            )
            - self.news.min_loc[1],
            "mon": self.display_identify,
        }

    def full_area(self) -> dict:
        return {
            "top": self.aspect_ratio.top,
            "left": self.aspect_ratio.left,
            "width": self.aspect_ratio.width,
            "height": self.aspect_ratio.height,
            "mon": self.display_identify,
        }
