from typing import List, Tuple, Dict, Any
from gbf_automata.models.image import ImageModel
from gbf_automata.models.display import DisplayModel
from gbf_automata.enums.template_match import TemplateMatch


class GameArea:
    def __init__(
        self,
        aspect_ratio: Dict[str, Any],
        top_left: ImageModel,
        bottom_right: ImageModel,
    ) -> None:
        self.top_left: ImageModel = top_left
        self.bottom_right: ImageModel = bottom_right
        self.aspect_ratio = DisplayModel(**aspect_ratio)

    # Display
    ##########################################################################
    #               (top)
    #                 |
    #                 |
    #                 v  (Game Area)
    #       (left) -> +--------------+
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

    def area(self) -> Dict[str, Any]:
        top_loc = self.top_left.max_loc
        bottom_loc = self.bottom_right.max_loc

        if self.top_left.method in [
            TemplateMatch.TM_SQDIFF,
            TemplateMatch.TM_SQDIFF_NORMED,
        ]:
            top_loc = self.top_left.min_loc
            bottom_loc = self.bottom_right.min_loc

        return {
            "top": self.aspect_ratio.top + top_loc[1],
            "left": self.aspect_ratio.left + top_loc[0],
            "width": self.aspect_ratio.width
            - (self.aspect_ratio.width - (bottom_loc[0] + self.bottom_right.template_width))
            - top_loc[0],
            "height": self.aspect_ratio.height
            - (self.aspect_ratio.height - (bottom_loc[1] + self.bottom_right.template_height))
            - top_loc[1],
        }

    def accuracy(self) -> List[Tuple[str, float]]:
        return [("top", self.top_left.accuracy()), ("bottom", self.bottom_right.accuracy())]

    def display_area(self) -> Dict[str, Any]:
        return {
            "top": self.aspect_ratio.top,
            "left": self.aspect_ratio.left,
            "width": self.aspect_ratio.width,
            "height": self.aspect_ratio.height,
        }

    def correction(self) -> Tuple[float, float]:
        top_loc = self.top_left.max_loc

        if self.top_left.method in [
            TemplateMatch.TM_SQDIFF,
            TemplateMatch.TM_SQDIFF_NORMED,
        ]:
            top_loc = self.top_left.min_loc

        return (self.aspect_ratio.left + top_loc[0], self.aspect_ratio.top + top_loc[1])
