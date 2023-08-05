import cv2 as cv
import numpy as np
import mss
from typing import List

from numpy.random import f

from gbf_automata.classes.game_area import GameArea
from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.util.settings import settings

class GBFGame:

    def __init__(self):
        self._method = TemplateMatch.TM_SQDIFF_NORMED
        self._game_area = None

        self._calibrate_game_area()

    def _calibrate_game_area(self) -> bool:        
            
        image_menu = cv.imread(settings.image_menu, cv.IMREAD_UNCHANGED)    
        image_news = cv.imread(settings.image_news, cv.IMREAD_UNCHANGED)
        image_home = cv.imread(settings.image_home, cv.IMREAD_UNCHANGED)
     
        w_menu, h_menu = image_menu.shape[::-1]
        w_news, h_news = image_news.shape[::-1]
        w_home, h_home = image_home.shape[::-1]

        search: List = []

        with mss.mss() as sct:
            
            for index, monitor in enumerate(sct.monitors[1:]):
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

                min_val_menu, max_val_menu, min_loc_menu, max_loc_menu = cv.minMaxLoc(res_menu)
                min_val_news, max_val_news, min_loc_news, max_loc_news = cv.minMaxLoc(res_news)
                min_val_home, max_val_home, min_loc_home, max_loc_home = cv.minMaxLoc(res_home)

                search.append(
                    GameArea(
                        display_identify=(index + 1),
                        aspect_ratio=monitor,
                        method=self._method,
                        menu_accuracy=(1 - min_val_menu),
                        news_accuracy=(1 - min_val_news),
                        home_accuracy=(1 - min_val_home)
                    )
                )

            result = max(search, key=lambda game_area: game_area.accuracy())

        return False


if __name__ == "__main__":
     game = GBFGame()
       
