from pydantic import BaseModel
from typing import Tuple
from gbf_automata.enums.template_match import TemplateMatch

class ImageModel(BaseModel):
    method: TemplateMatch
    image_width: int
    image_height: int
    min_val: float
    max_val: float
    min_loc: Tuple
    max_loc: Tuple

    correction: Tuple

    def plot_area(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
            if self.method in [TemplateMatch.TM_SQDIFF, TemplateMatch.TM_SQDIFF_NORMED]:
                top_left = (self.min_loc[0] - self.correction[0], self.min_loc[1] - self.correction[1])
            else:   
                top_left = (self.max_loc[0] - self.correction[0], self.max_loc[1] + self.correction[1])

            bottom_right = (top_left[0] + self.image_width, top_left[1] + self.image_height)

            return (top_left, bottom_right)


    def accuracy(self) -> float:
        return (1 - self.min_val)
