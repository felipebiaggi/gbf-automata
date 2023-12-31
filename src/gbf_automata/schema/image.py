import numpy as np
from typing import Tuple
from cv2.typing import Point
from pydantic import BaseModel
from gbf_automata.util.rng import rng
from gbf_automata.enums.template_match import TemplateMatch


class ImageModel(BaseModel):
    method: TemplateMatch
    image_width: int
    image_height: int
    min_val: float
    max_val: float
    min_loc: Point
    max_loc: Point

    correction: Point = (0, 0)

    def plot_area(self) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        if self.method in [TemplateMatch.TM_SQDIFF, TemplateMatch.TM_SQDIFF_NORMED]:
            top_left = (
                self.min_loc[0] - self.correction[0],
                self.min_loc[1] - self.correction[1],
            )
        else:
            top_left = (
                self.max_loc[0] - self.correction[0],
                self.max_loc[1] - self.correction[1],
            )

        bottom_right = (top_left[0] + self.image_width, top_left[1] + self.image_height)

        return (top_left, bottom_right)

    def accuracy(self) -> float:
        if self.method in [TemplateMatch.TM_SQDIFF, TemplateMatch.TM_SQDIFF_NORMED]:
            return 1 - self.min_val

        return self.max_val

    def center(self, correction: bool = False) -> Tuple[float, float]:
        min_loc = self.min_loc
        max_loc = self.max_loc

        if correction:
            min_loc = (min_loc[0] + self.correction[0], min_loc[1] + self.correction[1])

            max_loc = (max_loc[0] + self.correction[0], max_loc[1] + self.correction[1])

        if self.method in [TemplateMatch.TM_SQDIFF, TemplateMatch.TM_SQDIFF_NORMED]:
            return (
                np.trunc(min_loc[0] + (self.image_width * rng.random())),
                np.trunc(min_loc[1] + (self.image_height * rng.random())),
            )

        return (
            np.trunc(max_loc[0] + (self.image_width * rng.random())),
            np.trunc(max_loc[1] + (self.image_height * rng.random())),
        )
