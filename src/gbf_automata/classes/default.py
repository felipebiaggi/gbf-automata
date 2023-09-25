from typing import Tuple, List
from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.schema.display_schema import DisplayModel
from gbf_automata.schema.image_schema import ImageModel


class Default:
    def __init__(
        self,
        aspect_ratio: dict,
        menu: ImageModel,
        top_left_home: ImageModel,
        bottom_right_home: ImageModel,
    ) -> None:
        self.aspect_ratio = DisplayModel(**aspect_ratio)
        self.menu: ImageModel = menu
        self.top_left_home: ImageModel = top_left_home
        self.bottom_right_home: ImageModel = bottom_right_home

    def accuracy(self) -> List[Tuple[str, float]]:
        return [
            ("top_left_home", self.top_left_home.accuracy()),
            ("bottom_right_home", self.bottom_right_home.accuracy()),
            ("nemu", self.menu.accuracy()),
        ]

    def game_area(self) -> dict:
        menu_loc = self.menu.max_loc
        top_left_home_loc = self.top_left_home.max_loc
        bottom_right_home_loc = self.bottom_right_home.max_loc

        if self.top_left_home.method in [
            TemplateMatch.TM_SQDIFF,
            TemplateMatch.TM_SQDIFF_NORMED,
        ]:
            menu_loc = self.menu.min_loc
            top_left_home_loc = self.top_left_home.min_loc
            bottom_right_home_loc = self.bottom_right_home.min_loc

        return {
            "top": self.aspect_ratio.top + top_left_home_loc[1],
            "left": self.aspect_ratio.left + top_left_home_loc[0],
            "width": self.aspect_ratio.width
            - (self.aspect_ratio.width - (menu_loc[0] + self.menu.image_width))
            - top_left_home_loc[0],
            "height": self.aspect_ratio.height
            - (
                self.aspect_ratio.height
                - (bottom_right_home_loc[1] + self.bottom_right_home.image_height)
            )
            - top_left_home_loc[1],
            "mon": 1,
        }

    def full_area(self) -> dict:
        return {
            "top": self.aspect_ratio.top,
            "left": self.aspect_ratio.left,
            "width": self.aspect_ratio.width,
            "height": self.aspect_ratio.height,
        }
