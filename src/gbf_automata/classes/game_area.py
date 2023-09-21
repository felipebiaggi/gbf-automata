from gbf_automata.enums.template_match import TemplateMatch
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
            f"Display ID {self.display_identify} " f"Aspect Ratio {self.aspect_ratio} "
        )

    def accuracy(self) -> List[Tuple[str, float]]:
        return [
            ("menu", self.menu.accuracy()),
            ("news", self.news.accuracy()),
            ("home", self.home.accuracy()),
            ("back", self.back.accuracy()),
            ("reload", self.reload.accuracy()),
        ]

        ### Display ###

    ##########################################################################
    #
    #                    (Game Area)
    #  (top,     ) -> +--------------+
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
        news_loc = self.news.max_loc
        menu_loc = self.menu.max_loc
        home_loc = self.home.max_loc

        if self.news.method in [TemplateMatch.TM_SQDIFF, TemplateMatch.TM_SQDIFF_NORMED]:
            news_loc = self.news.min_loc
            menu_loc = self.menu.min_loc 
            home_loc = self.home.min_loc

        return {
                "top": self.aspect_ratio.top + news_loc[1],
                "left": self.aspect_ratio.left + news_loc[0],
                "width": self.aspect_ratio.width
                - (self.aspect_ratio.width - (menu_loc[0] + self.menu.image_width))
                - news_loc[0],
                "height": self.aspect_ratio.height
                - (
                    self.aspect_ratio.height
                    - (home_loc[1] + self.home.image_height)
                )
                - news_loc[1],
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
