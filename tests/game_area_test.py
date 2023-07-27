import argparse
import cv2 as cv
import numpy as np
import mss
from typing import List
from gbf_automata.classes.game_area import GameArea
from gbf_automata.enums import template_match
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
            display_template = np.asarray(
                sct.grab(monitor)
            )

            display_template = cv.cvtColor(
                src=display_template,
                code=cv.COLOR_RGBA2GRAY
            )

            res_menu = cv.matchTemplate(
                image=image_menu,
                templ=display_template,
                method=MATCH_METHOD
            )

            res_news = cv.matchTemplate(
                image=image_news,
                templ=display_template,
                method=MATCH_METHOD
            )

            res_home = cv.matchTemplate(
                image=image_home,
                templ=display_template,
                method=MATCH_METHOD
            )

            min_val_menu, _, min_loc_menu, _ = cv.minMaxLoc(res_menu)
            min_val_news, _, min_loc_news, _ = cv.minMaxLoc(res_news)
            min_val_home, _, min_loc_home, _ = cv.minMaxLoc(res_home)


            search.append(
                GameArea(
                    display_identify=(index + 1),
                    aspect_ratio=monitor,
                    method=MATCH_METHOD,
                    menu_accuracy=(1 - min_val_menu),
                    news_accuracy=(1 - min_val_news),
                    home_accuracy=(1 - min_val_home)
                )
            )

        result = max(
            search, key=lambda game_area: game_area.accuracy()
        )

        print(result)

    



