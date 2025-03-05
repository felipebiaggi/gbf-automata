from __future__ import annotations
import mss
import time
import cv2 as cv
import numpy as np
import pyautogui
from cv2.typing import Point
from typing import List, Optional
from gbf_automata.classes.load_state import LoadState
from gbf_automata.enums.state import State

from gbf_automata.util.logger import get_logger
from gbf_automata.util.settings import settings
from gbf_automata.classes.game_area import GameArea
from gbf_automata.enums.content_type import ContentType
from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.schema.data import data_model
from gbf_automata.schema.image import ImageModel
from gbf_automata.game.content.arcarum_v2 import ArcarumV2
from gbf_automata.exception.gbf_automata_exception import GBFAutomataError


logger = get_logger(__name__)


class GBFGame:
    def __init__(self, load_state: LoadState) -> None:
        self.max_attemps: int = 5
        self.area: Optional[GameArea]
        self.correction: Point = (0, 0)
        self.content: ContentType = settings.content_type
        self.method: TemplateMatch = TemplateMatch.TM_CCOEFF_NORMED

        # States
        self.load_state = load_state
        self.calibration_state: bool = False

    def search_for_element(
        self,
        element: str,
        correction: Point = (0, 0),
        error_ignore: bool = False,
        accuracy_threshold: float = 0.90,
        method: TemplateMatch = TemplateMatch.TM_CCOEFF_NORMED,
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

              p

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

                    if (not error_ignore) & (
                        image_model.accuracy() < accuracy_threshold
                    ):
                        raise GBFAutomataError(
                            f"Accuracy Error - Threshold: <{accuracy_threshold}> - Mensured: <{image_model.accuracy()}> - Element: <{element}>"
                        )

                    return image_model

        raise GBFAutomataError(f"Invalid image path: <{element}>")

    def search_for_element_and_scroll(
        self, element: str, accuracy_threshold: float = 0.90
    ) -> None:
        for _ in range(0, self.max_attemps):
            image = self.search_for_element(element=element, error_ignore=True)

            if image.accuracy() <= accuracy_threshold:
                pyautogui.scroll(-5)
                self.wait()
            else:
                pyautogui.moveTo(*image.center())
                pyautogui.click()
                self.wait()
                break

        def move_to_main_page(self) -> None:
            home_image_model = self.search_for_element(
                element=data_model.main.hohome_bottom,
            )

            pyautogui.moveTo(*home_image_model.center())

            pyautogui.click()

    def calibrate(self, home: bool = False, accuracy_threshold: float = 0.90) -> None:
        if home:
            image_top = cv.imread(data_model.main.news, cv.IMREAD_UNCHANGED)
        else:
            image_top = cv.imread(data_model.main.home_top, cv.IMREAD_UNCHANGED)

        image_bottom = cv.imread(data_model.main.home_bottom, cv.IMREAD_UNCHANGED)

        w_top, h_top = image_top.shape[::-1]
        w_bottom, h_bottom = image_bottom.shape[::-1]

        search: List[GameArea] = []

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

                min_val_top, max_val_top,min_loc_top, max_loc_top = cv.minMaxLoc(
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
            if accuracy < accuracy_threshold:
                raise GBFAutomataError(
                    f"Accuracy Error - Threshold: <{accuracy_threshold}> - Mensured: <{accuracy}> - Element: <{name}>"
                )

        self.calibration_state = True

        self.game_area = result

    def wait(self) -> None:
        while True:
            if self.load_state.get_state() == State.NONE:
                break
            time.sleep(1)
            logger.info(f"State: <{self.load_state.get_state()}>")
        time.sleep(0.5)

    def run(self) -> None:
        self.move_to_main_page()

        self.wait()
        self.calibrate(home=True)

        if settings.content_type == ContentType.ARCARUM_V2:
            arcarum_v2 = ArcarumV2(game=self)

            arcarum_v2.start()
