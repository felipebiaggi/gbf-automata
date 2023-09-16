from pprint import pprint
import cv2 as cv
from matplotlib import logging
import numpy as np
import mss
import time
from typing import List, Union

from gbf_automata.classes.game_area import GameArea
from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.schema.image_area import ImageModel
from gbf_automata.util.settings import settings
from gbf_automata.util.logger import get_logger
from gbf_automata.exception.gbf_automata_exception import GBFAutomataError

logger = get_logger(__name__)


class GBFGame:
    def __init__(self):
        self._method = TemplateMatch.TM_SQDIFF_NORMED
        self._game_area: Union[None, GameArea] = None
        self._min_accuracy = 0.85

        self._calibrate_game_area()

    def get_area(self) -> dict:
        if self._game_area:
            return self._game_area.area()

        return {}

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
            for index, monitor in enumerate(sct.monitors[2:]):
                display_template = np.asarray(sct.grab(monitor))

                display_template = cv.cvtColor(
                    src=display_template, code=cv.COLOR_RGBA2GRAY
                )

                res_menu = cv.matchTemplate(
                    image=image_menu, templ=display_template, method=self._method
                )

                res_news = cv.matchTemplate(
                    image=image_news, templ=display_template, method=self._method
                )

                res_home = cv.matchTemplate(
                    image=image_home, templ=display_template, method=self._method
                )

                res_back = cv.matchTemplate(
                    image=image_back, templ=display_template, method=self._method
                )

                res_reload = cv.matchTemplate(
                    image=image_reload, templ=display_template, method=self._method
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

                menu_model = ImageModel(
                    method=self._method,
                    image_width=w_menu,
                    image_height=h_menu,
                    min_val=min_val_menu,
                    max_val=max_val_menu,
                    min_loc=min_loc_menu,
                    max_loc=max_loc_menu,
                    correction=min_loc_news,
                )

                news_model = ImageModel(
                    method=self._method,
                    image_width=w_news,
                    image_height=h_news,
                    min_val=min_val_news,
                    max_val=max_val_news,
                    min_loc=min_loc_news,
                    max_loc=max_loc_news,
                    correction=min_loc_news,
                )

                home_model = ImageModel(
                    method=self._method,
                    image_width=w_home,
                    image_height=h_home,
                    min_val=min_val_home,
                    max_val=max_val_home,
                    min_loc=min_loc_home,
                    max_loc=max_loc_home,
                    correction=min_loc_news,
                )

                back_model = ImageModel(
                    method=self._method,
                    image_width=w_back,
                    image_height=h_back,
                    min_val=min_val_back,
                    max_val=max_val_back,
                    min_loc=min_loc_back,
                    max_loc=max_loc_back,
                    correction=min_loc_news
                )

                reload_model = ImageModel(
                    method=self._method,
                    image_width=w_reload,
                    image_height=h_reload,
                    min_val=min_val_reload,
                    max_val=max_val_reload,
                    min_loc=min_loc_reload,
                    max_loc=max_loc_reload,
                    correction=min_loc_news
                )

                search.append(
                    GameArea(
                        display_identify=(index + 1),
                        aspect_ratio=monitor,
                        menu=menu_model,
                        home=home_model,
                        news=news_model,
                        back=back_model,
                        reload=reload_model
                    )
                )

        self._game_area = max(search, key=lambda game_area: game_area.accuracy())

        for accuracy in self._game_area.accuracy():
            if accuracy < self._min_accuracy:
                raise GBFAutomataError(
                    f"Accuracy Error - Threshold: <{self._min_accuracy}> - Mensured: <{accuracy}>"
                )

        logger.info(
            "#########################################################################################"
        )
        logger.info(f"Display Info: <{self._game_area}>")
        logger.info(f"Game Area: <{self._game_area.area()}>")
        logger.info(f"News Coordinates: <{self._game_area._news.plot_area()}>")
        logger.info(f"Menu Coordinates: <{self._game_area._menu.plot_area()}>")
        logger.info(f"Home Coordinates: <{self._game_area._home.plot_area()}>")
        logger.info(f"Back Coordinates: <{self._game_area._back.plot_area()}>")
        logger.info(f"Reload Coordinates: <{self._game_area._reload.plot_area()}>")
        logger.info(
            "#########################################################################################"
        )


if __name__ == "__main__":
    game = GBFGame()


# if __name__ == "__main__":
#     game = GBFGame()
#
#     while True:
#         last_time = time.time()
#
#         with mss.mss() as sct:
#
#             img = sct.grab(game.get_area())
#
#             img_show = np.asarray(img)
#
#             menu_top_left, menu_bottom_right = game._game_area._menu.plot_area()
#
#             cv.rectangle(img_show, menu_top_left, menu_bottom_right, (0, 0, 255), 2)
#
#             news_top_left, news_bottom_right = game._game_area._news.plot_area()
#
#             cv.rectangle(img_show, news_top_left , news_bottom_right, (0, 0, 255), 2)
#
#             home_top_left, home_bottom_right = game._game_area._home.plot_area()
#
#             cv.rectangle(img_show, home_bottom_right, home_top_left, (0, 0, 255), 2)
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
