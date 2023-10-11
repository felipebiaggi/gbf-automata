from cv2.typing import Point
import mss
import time
import pyautogui
import cv2 as cv
import numpy as np
from typing import List

from gbf_automata.classes.game_area import GameArea
from gbf_automata.enums.template_match import TemplateMatch
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

        self.area = None

        # States
        self.state_calibration: bool = False

    def search_for_element(
        self,
        element: str,
        method: TemplateMatch = TemplateMatch.TM_CCOEFF_NORMED,
        accuracy_threshold: float = 0.95,
        correction: Point = (0, 0),
    ) -> ImageModel:
        if element:
            image = cv.imread(element, cv.IMREAD_UNCHANGED)
            w_image, h_image = image.shape[::-1]

            with mss.mss() as sct:
                for monitor in sct.monitors:
                    template = cv.cvtColor(
                        src=np.asarray(
                            sct.grab(monitor)
                        ), 
                        code=cv.COLOR_RGBA2GRAY
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
                    src=np.asarray(
                        sct.grab(monitor)
                    ),
                    code=cv.COLOR_RGBA2GRAY
                )

                res_image_top = cv.matchTemplate(
                    image=image_top,
                    templ=template,
                    method=self.method
                )

                res_image_bottom = cv.matchTemplate(
                    image=image_bottom,
                    templ=template,
                    method=self.method
                )


                min_val_top, max_val_top, min_loc_top, max_loc_top = cv.minMaxLoc(
                    res_image_top
                )

                min_val_bottom, max_val_bottom, min_loc_bottom, max_loc_bottom = cv.minMaxLoc(
                    res_image_bottom
                )
    
                if self.method in [TemplateMatch.TM_SQDIFF, TemplateMatch.TM_SQDIFF_NORMED]:
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
                   max_loc=max_loc_top
                )   

                bottom = ImageModel(
                    method=self.method,
                    image_width=w_bottom,
                    image_height=h_bottom,
                    min_val=min_val_bottom,
                    max_val=max_val_bottom,
                    min_loc=min_loc_bottom,
                    max_loc=max_loc_bottom
                )

                search.append(
                    GameArea(
                        aspect_ratio=monitor,
                        top=top,
                        bottom=bottom
                    )
                )

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

    def start(self):

        self.move_to_main_page()
        self.wait(seconds=4.0)
        self.calibrate(
            home=True
        )

        if settings.content_type == ContentType.ARCARUM_V2:
            arcarum = None

            for _ in range(0, self.max_attemps):
                result = self.search_for_element(element=settings.image_arcarum)

                if result.accuracy() >= 0.95:
                    arcarum = result
                    break

                pyautogui.scroll(-5)

                self.wait(0.5)

            if not arcarum:
                raise GBFAutomataError("Arcarum banner not found.")

            pyautogui.moveTo(*arcarum.center(correction=True))

            pyautogui.click()

            self.wait(4.0)

            type_arcarum = self.search_for_element(
                element=settings.image_button_classic
            )

            if type_arcarum.accuracy() < 0.95:
                arcarum_sandbox = self.search_for_element(
                    element=settings.image_button_sandbox
                )

                if arcarum_sandbox.accuracy() < 0.95:
                    raise GBFAutomataError("Invalid page")

                pyautogui.moveTo(*arcarum_sandbox.center(correction=True))

                pyautogui.click()

            ### Select Stage

             


if __name__ == "__main__":
    game = GBFGame()
    game.start()
