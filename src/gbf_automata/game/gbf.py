from __future__ import annotations
from cv2.typing import Point
import mss
import time
import pyautogui
import cv2 as cv
import numpy as np
from typing import List, Tuple, Optional

from gbf_automata.data.arcarum_v2.coordinates import arcarum_v2_coordinates
from gbf_automata.classes.game_area import GameArea
from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.game.content.arcarum_v2 import ArcarumV2
from gbf_automata.schema.arcarum_v2 import ArcarumV2Model
from gbf_automata.schema.image_schema import ImageModel
from gbf_automata.util.settings import settings
from gbf_automata.util.logger import get_logger
from gbf_automata.exception.gbf_automata_exception import GBFAutomataError
from gbf_automata.enums.content_type import ContentType


logger = get_logger(__name__)


class GBFGame:
    def __init__(self):
        self.accuracy_threshold: float = 0.90
        self.correction: Point = (0, 0)
        self.method: TemplateMatch = TemplateMatch.TM_CCOEFF_NORMED
        self.content: ContentType = settings.content_type
        self.max_attemps: int = 5

        self.area: Optional[GameArea]

        # States
        self.state_calibration: bool = False

    def search_for_element(
        self,
        element: str,
        method: TemplateMatch = TemplateMatch.TM_CCOEFF_NORMED,
        correction: Point = (0, 0),
    ) -> ImageModel:
        if element:
            image = cv.imread(element, cv.IMREAD_UNCHANGED)
            w_image, h_image = image.shape[::-1]

            with mss.mss() as sct:
                for monitor in sct.monitors:
                    template = cv.cvtColor(
                        src=np.asarray(sct.grab(monitor)), code=cv.COLOR_RGBA2GRAY
                    )

                    res_element = cv.matchTemplate(
                        image=image, templ=template, method=method
                    )

                    (
                        min_val_image,
                        max_val_image,
                        min_loc_image,
                        max_loc_image,
                    ) = cv.minMaxLoc(res_element)

                    image_model = ImageModel(
                        method=method,
                        image_width=w_image,
                        image_height=h_image,
                        min_val=min_val_image,
                        max_val=max_val_image,
                        min_loc=min_loc_image,
                        max_loc=max_loc_image,
                        correction=correction,
                    )

                    return image_model

        raise GBFAutomataError(f"Invalid image path: <{element}>")

    def search_for_element_and_scroll(
        self,
        element: str,
    ):
        for _ in range(0, self.max_attemps):
            image = self.search_for_element(element=element)

            if image.accuracy() <= self.accuracy_threshold:
                pyautogui.scroll(-5)
                self.wait(0.5)
            else:
                pyautogui.moveTo(*image.center())
                pyautogui.click()
                self.wait(4.0)
                break

    def move_to_main_page(self):
        home_image_model = self.search_for_element(
            element=settings.image_home_bottom,
        )

        pyautogui.moveTo(*home_image_model.center())

        pyautogui.click()

    def calibrate(self, home: bool = False):
        if home:
            image_top = cv.imread(settings.image_news, cv.IMREAD_UNCHANGED)
        else:
            image_top = cv.imread(settings.image_home_top, cv.IMREAD_UNCHANGED)

        image_bottom = cv.imread(settings.image_home_bottom, cv.IMREAD_UNCHANGED)

        w_top, h_top = image_top.shape[::-1]
        w_bottom, h_bottom = image_bottom.shape[::-1]

        search: List = []

        with mss.mss() as sct:
            for monitor in sct.monitors:
                template = cv.cvtColor(
                    src=np.asarray(sct.grab(monitor)), code=cv.COLOR_RGBA2GRAY
                )

                res_image_top = cv.matchTemplate(
                    image=image_top, templ=template, method=self.method
                )

                res_image_bottom = cv.matchTemplate(
                    image=image_bottom, templ=template, method=self.method
                )

                min_val_top, max_val_top, min_loc_top, max_loc_top = cv.minMaxLoc(
                    res_image_top
                )

                (
                    min_val_bottom,
                    max_val_bottom,
                    min_loc_bottom,
                    max_loc_bottom,
                ) = cv.minMaxLoc(res_image_bottom)

                if self.method in [
                    TemplateMatch.TM_SQDIFF,
                    TemplateMatch.TM_SQDIFF_NORMED,
                ]:
                    self.correction = min_loc_top
                else:
                    self.correction = max_loc_top

                top = ImageModel(
                    method=self.method,
                    image_width=w_top,
                    image_height=h_top,
                    min_val=min_val_top,
                    max_val=max_val_top,
                    min_loc=min_loc_top,
                    max_loc=max_loc_top,
                )

                bottom = ImageModel(
                    method=self.method,
                    image_width=w_bottom,
                    image_height=h_bottom,
                    min_val=min_val_bottom,
                    max_val=max_val_bottom,
                    min_loc=min_loc_bottom,
                    max_loc=max_loc_bottom,
                )

                search.append(GameArea(aspect_ratio=monitor, top=top, bottom=bottom))

        result = max(search, key=lambda game_area: game_area.accuracy())

        for name, accuracy in result.accuracy():
            if accuracy < self.accuracy_threshold:
                raise GBFAutomataError(
                    f"Accuracy Error - Threshold: <{self.accuracy_threshold}> - Mensured: <{accuracy}> - Element: <{name}>"
                )

        self.state_calibration = True

        self.game_area = result

    def wait(self, seconds: float = 2.0):
        time.sleep(seconds)

    def arcarum_v2_node_coordinates(
        self, arcarum_v2: ArcarumV2Model
    ) -> Tuple[float, float]:
        coordinates = arcarum_v2_coordinates[arcarum_v2.zone]["stage"][
            arcarum_v2.subzone.stage
        ]["node"][arcarum_v2.subzone.node]

        game_area = self.area.correction()  # type: ignore

        return (coordinates[0] + game_area[0], coordinates[1] + game_area[1])

    def arcarum_v2_select_stage(self, arcarum_v2: ArcarumV2Model):
        image_back_result = self.search_for_element(element=settings.image_back_stage)

        image_forward_result = self.search_for_element(
            element=settings.image_forward_stage
        )

        if (
                image_back_result.accuracy() <= self.accuracy_threshold <= image_forward_result.accuracy()
        ):
            logger.info("Already at the correct Stage!")
            return

        if image_back_result.accuracy() >= self.accuracy_threshold:
            pyautogui.moveTo(*image_back_result.center())
            pyautogui.click()
            self.wait(0.5)
            pyautogui.click()

        for _ in range(1, arcarum_v2.subzone.stage):
            pyautogui.moveTo(*image_forward_result.center())
            pyautogui.click()
            self.wait(0.5)

        pyautogui.moveTo(*self.arcarum_v2_node_coordinates(arcarum_v2=arcarum_v2))

        pyautogui.click()

    def start(self):
        self.move_to_main_page()

        self.wait(seconds=4.0)
        self.calibrate(home=True)

        if settings.content_type == ContentType.ARCARUM_V2:
            arcarum_v2 = ArcarumV2(game=self)

            arcarum_v2.start()
