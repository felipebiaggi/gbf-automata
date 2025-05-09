from typing import Tuple

import numpy as np
from cv2.typing import Point

from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.util.logger import get_logger
from gbf_automata.util.rng import rng_uniform

logger = get_logger()


class ImageModel:
    def __init__(
        self,
        method: TemplateMatch,
        template_width: int,
        template_height: int,
        min_val: float,
        max_val: float,
        min_loc: Point,
        max_loc: Point,
        correction: Point = (0, 0),
    ):
        self.method: TemplateMatch = method
        self.template_width: int = template_width
        self.template_height: int = template_height
        self.min_val: float = min_val
        self.max_val: float = max_val
        self.min_loc: Point = min_loc
        self.max_loc: Point = max_loc
        self.correction: Point = correction

    def __str__(self):
        return (
            f"ImageModel(\n"
            f"  Method:          {self.method}\n"
            f"  Template Size:   {self.template_width} x {self.template_height}\n"
            f"  Min Val:         {self.min_val:.4f}\n"
            f"  Max Val:         {self.max_val:.4f}\n"
            f"  Min Loc:         {self.min_loc}\n"
            f"  Max Loc:         {self.max_loc}\n"
            f"  Correction:      {self.correction}\n)"
        )

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

        bottom_right = (
            top_left[0] + self.template_width,
            top_left[1] + self.template_height,
        )

        return (top_left, bottom_right)

    def accuracy(self) -> float:
        if self.method in [TemplateMatch.TM_SQDIFF, TemplateMatch.TM_SQDIFF_NORMED]:
            return 1 - self.min_val

        return self.max_val

    def center(self, correction: bool = False) -> Tuple[float, float]:
        min_loc = self.min_loc
        max_loc = self.max_loc

        offset_widht = rng_uniform(10)
        offset_height = rng_uniform(10)

        if correction:
            min_loc = (min_loc[0] + self.correction[0], min_loc[1] + self.correction[1])
            max_loc = (max_loc[0] + self.correction[0], max_loc[1] + self.correction[1])

        if self.method in [TemplateMatch.TM_SQDIFF, TemplateMatch.TM_SQDIFF_NORMED]:
            width = np.trunc(min_loc[0] + (self.template_width / 2)) + offset_widht
            height = np.trunc(min_loc[1] + (self.template_height / 2)) + offset_height

            logger.debug(f"[IMAGE MODEL] Width: {width} - Height: {height}")
            return width, height

        width = np.trunc(max_loc[0] + (self.template_width / 2)) + offset_widht
        height = np.trunc(max_loc[1] + (self.template_height / 2)) + offset_height

        logger.debug(f"[IMAGE MODEL] Width: {width} - Height: {height}")
        return width, height
