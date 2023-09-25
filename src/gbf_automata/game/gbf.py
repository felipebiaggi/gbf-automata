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
        self.accuracy_threshold: float = 0.95
        self.correction: Point = (0, 0)

        self.method: TemplateMatch = TemplateMatch.TM_CCOEFF_NORMED
        self.max_attemps: int = 5
        self.state_calibration: bool = False
        self.content: ContentType = settings.content_type

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
                for monitor in sct.monitors[1:]:
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

                    if image_model.accuracy() >= accuracy_threshold:
                        return image_model

                    raise GBFAutomataError(
                        f"Accuracy below the required threshold: <{image_model.accuracy()}>"
                    )

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
                    self.correction=

                self.correction = 

                top = ImageModel(
                   method=self.method, 
                )


    # Abstraction leak???
    # TODO: refactory
    def _calibrate_game_area(self):
        image_menu = cv.imread(settings.image_menu, cv.IMREAD_UNCHANGED)
        image_news = cv.imread(settings.image_news, cv.IMREAD_UNCHANGED)
        image_home = cv.imread(settings.image_home, cv.IMREAD_UNCHANGED)
        image_back = cv.imread(settings.image_back, cv.IMREAD_UNCHANGED)
        image_reload = cv.imread(settings.image_reload, cv.IMREAD_UNCHANGED)

        w_menu, h_menu = image_menu.shape[::-1]
        w_news, h_news = image_news.shape[::-1]
        w_home, h_home = image_home.shape[::-1]
        w_back, h_back = image_back.shape[::-1]
        w_reload, h_reload = image_reload.shape[::-1]

        search: List = []

        with mss.mss() as sct:
            for index, monitor in enumerate(sct.monitors[:1]):
                display_template = np.asarray(sct.grab(monitor))

                display_template = cv.cvtColor(
                    src=display_template, code=cv.COLOR_RGBA2GRAY
                )

                res_menu = cv.matchTemplate(
                    image=image_menu, templ=display_template, method=self.method
                )

                res_news = cv.matchTemplate(
                    image=image_news, templ=display_template, method=self.method
                )

                res_home = cv.matchTemplate(
                    image=image_home, templ=display_template, method=self.method
                )

                res_back = cv.matchTemplate(
                    image=image_back, templ=display_template, method=self.method
                )

                res_reload = cv.matchTemplate(
                    image=image_reload, templ=display_template, method=self.method
                )

                min_val_menu, max_val_menu, min_loc_menu, max_loc_menu = cv.minMaxLoc(
                    res_menu
                )
                min_val_news, max_val_news, min_loc_news, max_loc_news = cv.minMaxLoc(
                    res_news
                )
                min_val_home, max_val_home, min_loc_home, max_loc_home = cv.minMaxLoc(
                    res_home
                )
                min_val_back, max_val_back, min_loc_back, max_loc_back = cv.minMaxLoc(
                    res_back
                )
                (
                    min_val_reload,
                    max_val_reload,
                    min_loc_reload,
                    max_loc_reload,
                ) = cv.minMaxLoc(res_reload)

                if self.method in [
                    TemplateMatch.TM_SQDIFF_NORMED,
                    TemplateMatch.TM_SQDIFF,
                ]:
                    self._correction = min_loc_news
                else:
                    self._correction = max_loc_news

                menu_model = ImageModel(
                    method=self.method,
                    image_width=w_menu,
                    image_height=h_menu,
                    min_val=min_val_menu,
                    max_val=max_val_menu,
                    min_loc=min_loc_menu,
                    max_loc=max_loc_menu,
                    correction=self._correction,
                )

                news_model = ImageModel(
                    method=self.method,
                    image_width=w_news,
                    image_height=h_news,
                    min_val=min_val_news,
                    max_val=max_val_news,
                    min_loc=min_loc_news,
                    max_loc=max_loc_news,
                    correction=self._correction,
                )

                home_model = ImageModel(
                    method=self.method,
                    image_width=w_home,
                    image_height=h_home,
                    min_val=min_val_home,
                    max_val=max_val_home,
                    min_loc=min_loc_home,
                    max_loc=max_loc_home,
                    correction=self._correction,
                )

                back_model = ImageModel(
                    method=self.method,
                    image_width=w_back,
                    image_height=h_back,
                    min_val=min_val_back,
                    max_val=max_val_back,
                    min_loc=min_loc_back,
                    max_loc=max_loc_back,
                    correction=self._correction,
                )

                reload_model = ImageModel(
                    method=self.method,
                    image_width=w_reload,
                    image_height=h_reload,
                    min_val=min_val_reload,
                    max_val=max_val_reload,
                    min_loc=min_loc_reload,
                    max_loc=max_loc_reload,
                    correction=self._correction,
                )

                search.append(
                    Home(
                        display_identify=(index + 1),
                        aspect_ratio=monitor,
                        menu=menu_model,
                        home=home_model,
                        news=news_model,
                        back=back_model,
                        reload=reload_model,
                    )
                )

        result = max(search, key=lambda game_area: game_area.accuracy())

        for name, accuracy in result.accuracy():
            if accuracy < self._min_accuracy:
                raise GBFAutomataError(
                    f"Accuracy Error - Threshold: <{self._min_accuracy}> - Mensured: <{accuracy}> - Element: <{name}>"
                )

        logger.info(
            "#########################################################################################"
        )
        logger.info(f"Display Info: <{result}>")
        logger.info(f"Game Area: <{result.game_area()}>")
        logger.info(f"News Coordinates: <{result.news.plot_area()}>")
        logger.info(f"Menu Coordinates: <{result.menu.plot_area()}>")
        logger.info(f"Home Coordinates: <{result.home.plot_area()}>")
        logger.info(f"Back Coordinates: <{result.back.plot_area()}>")
        logger.info(f"Reload Coordinates: <{result.reload.plot_area()}>")

        self.state_calibration = True

        return result

    def move_to_home_page(self):
        logger.info(
            "#########################################################################################"
        )
        logger.info(f"Mouse start position: <{pyautogui.position()}>")
        logger.info(
            "Move to Home: x: <{}> | y: <{}>".format(*self.game_area.home.center())
        )

        pyautogui.moveTo(*self.game_area.home.center())

        pyautogui.click()

        # TODO: Implement better wait method
        self.wait(4.0)

    def wait(self, seconds: float = 2.0):
        time.sleep(seconds)

    def start(self):
        self.move_to_home_page()

        if settings.content_type == ContentType.GW:
            gw = None

            for _ in range(0, self.max_attemps):
                result = self.search_for_element(element=settings.image_gw)

                print(f"accuracy: <{result.accuracy()}>")

                if result.accuracy() >= 0.95:
                    gw = result
                    break

                pyautogui.scroll(-5)

            if not gw:
                raise GBFAutomataError("Arcarum banner not found.")

            logger.info(
                "Movo to GW: x: <{}> | y: <{}>".format(*gw.center(correction=True))
            )

            pyautogui.moveTo(*gw.center(correction=True))

            pyautogui.click()

            self.wait(4.0)

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

            print("PASSOUUUUUUU")


if __name__ == "__main__":
    game = GBFGame()
    game.move_to_main_page()
