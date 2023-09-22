import argparse
import cv2 as cv
import numpy as np
import mss
from typing import List
from gbf_automata.classes.home import Home
from gbf_automata.enums.template_match import TemplateMatch

from pathvalidate.argparse import sanitize_filepath_arg

parse = argparse.ArgumentParser()

parse.add_argument("-m", "--menu", type=sanitize_filepath_arg, required=True)
parse.add_argument("-n", "--news", type=sanitize_filepath_arg, required=True)
parse.add_argument("-o", "--home", type=sanitize_filepath_arg, required=True)


MATCH_METHOD = TemplateMatch.TM_CCOEFF_NORMED

if __name__ == "__main__":
    args = parse.parse_args()

    image_menu = cv.imread(args.menu, cv.IMREAD_UNCHANGED)
    image_news = cv.imread(args.news, cv.IMREAD_UNCHANGED)
    image_home = cv.imread(args.home, cv.IMREAD_UNCHANGED)

    w_menu, h_menu = image_menu.shape[::-1]
    w_news, h_news = image_news.shape[::-1]
    w_home, h_home = image_home.shape[::-1]

    with mss.mss() as sct:
        search: List = []

        for index, monitor in enumerate(sct.monitors[1:]):
            display_template = np.asarray(sct.grab(monitor))

            display_template = cv.cvtColor(
                src=display_template, code=cv.COLOR_RGBA2GRAY
            )

            res_menu = cv.matchTemplate(
                image=image_menu, templ=display_template, method=method
            )

            res_news = cv.matchTemplate(
                image=image_news, templ=display_template, method=method
            )

            res_home = cv.matchTemplate(
                image=image_home, templ=display_template, method=method
            )

            res_back = cv.matchTemplate(
                image=image_back, templ=display_template, method=method
            )

            res_reload = cv.matchTemplate(
                image=image_reload, templ=display_template, method=method
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
