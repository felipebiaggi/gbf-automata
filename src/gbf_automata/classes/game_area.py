from typing import List, Tuple
from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.schema.display_schema import DisplayModel
from gbf_automata.schema.image_schema import ImageModel


class GameArea:
    def __init__(
        self,
        aspect_ratio: dict,
        top: ImageModel,
        bottom: ImageModel,
    ) -> None: 
        self.aspect_ratio = DisplayModel(**aspect_ratio)
        self.top: ImageModel = top
        self.bottom: ImageModel = bottom
    

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
        top_loc = self.top.max_loc
        bottom_loc = self.bottom.max_loc

        if self.top.method in [
            TemplateMatch.TM_SQDIFF,
            TemplateMatch.TM_SQDIFF_NORMED,
        ]:
            top_loc = self.top.min_loc
            bottom_loc = self.bottom.min_loc

        return {
            "top": self.aspect_ratio.top + top_loc[1],
            "left": self.aspect_ratio.left + top_loc[0],
            "width": self.aspect_ratio.width
            - (self.aspect_ratio.width - (bottom_loc[0] + self.bottom.image_width))
            - top_loc[0],
            "height": self.aspect_ratio.height
            - (self.aspect_ratio.height - (bottom_loc[1] + self.bottom.image_height))
            - top_loc[1],
        }

    
    def accuracy(self) -> List[Tuple[str, float]]:
        return [
            ("top", self.top.accuracy()), ("bottom", self.bottom.accuracy())
        ] 

    def display_area(self) -> dict:
        return {
            "top": self.aspect_ratio.top,
            "left": self.aspect_ratio.left,
            "width": self.aspect_ratio.width,
            "height": self.aspect_ratio.height,
        }   

    
    def correction(self) -> Tuple[float, float]:

        top_loc = self.top.max_loc

        if self.top.method in [
            TemplateMatch.TM_SQDIFF,
            TemplateMatch.TM_SQDIFF_NORMED,
        ]:
            top_loc = self.top.min_loc

        return (self.aspect_ratio.left + top_loc[0], self.aspect_ratio.top + top_loc[1])
