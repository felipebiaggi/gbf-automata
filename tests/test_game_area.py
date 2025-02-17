import mss
import cv2 as cv
import numpy as np
from pathlib import Path
from typing import List
from gbf_automata.classes.game_area import GameArea
from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.models.image import ImageModel

menu_dir = Path(__file__).parent.parent / "resources" / "main_menu"

template_menu_path = menu_dir / "template_menu_gray.png"
template_news_path = menu_dir / "template_news_gray.png"
template_home_bottom_path = menu_dir / "template_home_bottom_gray.png"
template_back_path = menu_dir / "template_back_gray.png"

MATCH_METHOD = TemplateMatch.TM_CCOEFF_NORMED

if __name__ == "__main__":
    template_menu = cv.imread(template_menu_path.as_posix(), cv.IMREAD_UNCHANGED)
    template_news = cv.imread(template_news_path.as_posix(), cv.IMREAD_UNCHANGED)
    template_home_bottom = cv.imread(
        template_home_bottom_path.as_posix(), cv.IMREAD_UNCHANGED
    )
    template_back = cv.imread(template_back_path.as_posix(), cv.IMREAD_UNCHANGED)

    template_menu_h, template_menu_w = template_menu.shape
    template_news_h, template_news_w = template_news.shape
    template_home_bottom_h, template_home_bottom_w = template_home_bottom.shape
    template_back_h, template_back_w = template_back.shape

    with mss.mss() as sct:
        search: List = []

        for index, monitor in enumerate(sct.monitors[0:1]):
            print(monitor)

            target_image = np.asarray(sct.grab(monitor))

            target_image_gray = cv.cvtColor(src=target_image, code=cv.COLOR_RGBA2GRAY)

            image_source = cv.cvtColor(src=target_image, code=cv.COLOR_RGBA2GRAY)

            res_menu = cv.matchTemplate(target_image_gray, template_menu, MATCH_METHOD)

            res_home_bottom = cv.matchTemplate(
                target_image_gray, template_home_bottom, MATCH_METHOD
            )

            res_news = cv.matchTemplate(target_image_gray, template_news, MATCH_METHOD)

            res_back = cv.matchTemplate(target_image_gray, template_back, MATCH_METHOD)

            min_val_menu, max_val_menu, min_loc_menu, max_loc_menu = cv.minMaxLoc(
                res_menu
            )

            min_val_news, max_val_news, min_loc_news, max_loc_news = cv.minMaxLoc(
                res_news
            )

            (
                min_val_home_bottom,
                max_val_home_bottom,
                min_loc_home_bottom,
                max_loc_home_bottom,
            ) = cv.minMaxLoc(res_home_bottom)

            min_val_back, max_val_back, min_loc_back, max_loc_back = cv.minMaxLoc(
                res_back
            )

            if MATCH_METHOD in [
                TemplateMatch.TM_SQDIFF_NORMED,
                TemplateMatch.TM_SQDIFF_NORMED,
            ]:
                correction = min_loc_news
            else:
                correction = max_loc_news

            menu_model = ImageModel(
                method=MATCH_METHOD,
                template_width=template_menu_w,
                template_height=template_menu_h,
                min_val=min_val_menu,
                max_val=max_val_menu,
                min_loc=min_loc_menu,
                max_loc=max_loc_menu,
            )

            news_model = ImageModel(
                method=MATCH_METHOD,
                template_width=template_news_w,
                template_height=template_news_h,
                min_val=min_val_news,
                max_val=max_val_news,
                min_loc=min_loc_news,
                max_loc=max_loc_news,
            )

            home_bottom_model = ImageModel(
                method=MATCH_METHOD,
                template_width=template_home_bottom_w,
                template_height=template_home_bottom_h,
                min_val=min_val_home_bottom,
                max_val=max_val_home_bottom,
                min_loc=min_loc_home_bottom,
                max_loc=max_loc_home_bottom,
            )

            back_model = ImageModel(
                method=MATCH_METHOD,
                template_width=template_back_w,
                template_height=template_back_h,
                min_val=min_val_back,
                max_val=max_val_back,
                min_loc=min_loc_back,
                max_loc=max_loc_back,
            )

            search.append(
                GameArea(
                    top_left=news_model,
                    bottom_right=home_bottom_model,
                    aspect_ratio=monitor,
                )
            )

        result: GameArea = max(search, key=lambda game_area: game_area.accuracy())

        game_area_image = np.asarray(sct.grab(result.area()))

        top_left, bottom_right = result.top_left.plot_area()

        print(result.top_left.plot_area())

        cv.namedWindow("Target:", cv.WINDOW_KEEPRATIO)
        cv.rectangle(game_area_image, top_left, bottom_right, (0, 0, 255), 4)
        cv.imshow("Target", game_area_image)

        while cv.getWindowProperty("Target", cv.WND_PROP_VISIBLE) >= 1:
            key = cv.waitKey(1000)
            if key == 27:
                break

        cv.destroyAllWindows()
