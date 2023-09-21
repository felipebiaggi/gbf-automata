from pprint import pprint
import cv2 as cv
from cv2.gapi.wip.draw import Image
from matplotlib import logging
import numpy as np
import mss
import time
from typing import List, Union
import pyautogui

from gbf_automata.classes.game_area import GameArea
from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.schema.image_area import ImageModel
from gbf_automata.util.settings import settings
from gbf_automata.util.logger import get_logger
from gbf_automata.exception.gbf_automata_exception import GBFAutomataError
from gbf_automata.enums.content_type import ContentType


logger = get_logger(__name__)


class GBFGame:
    def __init__(self):
        self._min_accuracy = 0.90
        self._correction = (0, 0)

        self.method = TemplateMatch.TM_CCOEFF_NORMED
        self.max_attemps = 5
        self.game_area: GameArea = self._calibrate_game_area()

    def get_area(self) -> dict:
        if self.game_area:
            return self.game_area.area()

        return {}

    # Abstraction leak???
    # TODO: refactory
    def _calibrate_game_area(self):
        image_menu = cv.imread(settings.image_menu, cv.IMREAD_UNCHANGED)
        image_news = cv.imread(settings.image_news, cv.IMREAD_UNCHANGED)
        image_home = cv.imread(settings.image_home, cv.IMREAD_UNCHANGED)
        image_back = cv.imread(settings.image_back, cv.IMREAD_UNCHANGED)
        # image_reload = cv.imread('resource/main_menu/image_arcarum_gray.png', cv.IMREAD_UNCHANGED)
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

                if self.method in [TemplateMatch.TM_SQDIFF_NORMED, TemplateMatch.TM_SQDIFF]:
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
                    GameArea(
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
        logger.info(f"Game Area: <{result.area()}>")
        logger.info(f"News Coordinates: <{result.news.plot_area()}>")
        logger.info(f"Menu Coordinates: <{result.menu.plot_area()}>")
        logger.info(f"Home Coordinates: <{result.home.plot_area()}>")
        logger.info(f"Back Coordinates: <{result.back.plot_area()}>")
        logger.info(f"Reload Coordinates: <{result.reload.plot_area()}>")

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

    def search_for_element(self, element: str):
        if element:
            image = cv.imread(element, cv.IMREAD_UNCHANGED)

            w_image, h_image = image.shape[::-1]

            with mss.mss() as sct:
                template = cv.cvtColor(
                    src=np.asarray(sct.grab(self.get_area())), code=cv.COLOR_RGBA2GRAY
                )

                res_element = cv.matchTemplate(
                    image=image, templ=template, method=self.method
                )

                (
                    min_val_image,
                    max_val_image,
                    min_loc_image,
                    max_loc_image,
                ) = cv.minMaxLoc(res_element)

                return ImageModel(
                    method=self.method,
                    image_width=w_image,
                    image_height=h_image,
                    min_val=min_val_image,
                    max_val=max_val_image,
                    min_loc=min_loc_image,
                    max_loc=max_loc_image,
                    correction=self._correction,
                )

        raise GBFAutomataError(f"Invalid image path: <{element}>")

    def start(self):
        self.move_to_home_page()

        if settings.content_type == ContentType.GW: 
            gw = None

            for _ in range(0, self.max_attemps):
                result = self.search_for_element(element=settings.image_gw)
                
                print(f'accuracy: <{result.accuracy()}>')

                if result.accuracy() >= 0.95:
                    gw = result
                    break
                
                pyautogui.scroll(-5)

            if not gw:
                raise GBFAutomataError("Arcarum banner not found.")

            logger.info("Movo to GW: x: <{}> | y: <{}>".format(*gw.center(correction=True)))

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

            if not arcarum:
                raise GBFAutomataError("Arcarum banner not found.")

            pyautogui.moveTo(*arcarum.center(correction=True))

            pyautogui.click()

            self.wait(4.0)

            # CHECK ARCARUM 

            type_arcarum = self.search_for_element(
                element=settings.image_button_classic 
            )

            if type_arcarum.accuracy() < 0.95:
                
                arcarum_sandbox = self.search_for_element(
                    element=settings.image_button_sandbox
                )

                if arcarum_sandbox.accuracy() < 0.95:
                    raise GBFAutomataError('Invalid page')

                pyautogui.moveTo(*arcarum_sandbox.center(correction=True))

                pyautogui.click()

            print("PASSOUUUUUUU")
             


if __name__ == "__main__":
    game = GBFGame()
    game.start()


# if __name__ == "__main__":
#     game = GBFGame()
#
#     # gw = game.search_for_element('resource/main_menu/image_gw_gray.png')
#
#     gw = cv.imread("resource/main_menu/image_gw_gray.png", cv.IMREAD_UNCHANGED)
#
#     w_gw, h_gw = gw.shape[::-1]
#
#     while True:
#         last_time = time.time()
#
#         with mss.mss() as sct:
#             img = sct.grab(
#                 game.get_area()
#             )
#
#             # img = sct.grab(
#             #     {
#             #         "left": 3840,
#             #         "top": 1080,
#             #         "width": 700,
#             #         "height": 1000,
#             #     }
#             # )
#
#             img_show = np.asarray(img)
#
#             img_show_gray = cv.cvtColor(src=img_show, code=cv.COLOR_RGBA2GRAY)
#
#             gw_match = cv.matchTemplate(
#                 image=gw, templ=img_show_gray, method=game.method
#             )
#
#             min_val_gw, max_val_gw, min_loc_gw, max_loc_gw = cv.minMaxLoc(gw_match)
#
#             top_left = max_loc_gw
#
#             bottom_right = (top_left[0] + w_gw, top_left[1] + h_gw)
#
#             menu_top_left, menu_bottom_right = game.game_area.menu.plot_area()
#
#             cv.rectangle(img_show, menu_top_left, menu_bottom_right, (0, 0, 255), 2)
#
#             news_top_left, news_bottom_right = game.game_area.news.plot_area()
#
#             cv.rectangle(img_show, news_top_left, news_bottom_right, (0, 0, 255), 2)
#             home_top_left, home_bottom_right = game.game_area.home.plot_area()
#
#             cv.rectangle(img_show, home_bottom_right, home_top_left, (0, 0, 255), 2)
#
#             back_top_left, back_bottom_right = game.game_area.back.plot_area()
#
#             cv.rectangle(img_show, back_top_left, back_bottom_right, (0, 0, 255), 2)
#
#             reload_top_left, reload_bottom_right = game.game_area.reload.plot_area()
#
#             cv.rectangle(img_show, reload_top_left, reload_bottom_right, (0, 0, 255), 2)
#
#             # gw_top_left, gw_bottom_right = gw.plot_area()
#             #
#             cv.rectangle(img_show, top_left, bottom_right, (0, 0, 255), 2)
#
#             cv.imshow("", img_show)
#
#             game._calibrate_game_area()
#
#             if cv.waitKey(25) & 0xFF == ord("q"):
#                 cv.destroyAllWindows
#                 break
#
#         logger.debug(f'fps: <{1 / (time.time() - last_time)}>')
