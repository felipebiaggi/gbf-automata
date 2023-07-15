import argparse
import time
import cv2 as cv
import numpy as np
from mss import mss
import mss.tools

from pathvalidate.argparse import sanitize_filepath_arg

parse = argparse.ArgumentParser()

parse.add_argument("-m", "--menu", type=sanitize_filepath_arg)

parse.add_argument("-n", "--news", type=sanitize_filepath_arg)

parse.add_argument("-o", "--home", type=sanitize_filepath_arg)


class CalibrationScreen:
    def __init__(
        self,
        display,
        aspect_ratio,
        menu_accuracy,
        news_accuracy,
        home_accuracy,
        top_left_width,
        top_left_height,
        top_right_width,
        bottom_right_height,
    ) -> None:
        self._display = display
        self._aspect_ratio = aspect_ratio
        self._menu_accuracy = menu_accuracy
        self._news_accuracy = news_accuracy
        self._home_accuracy = home_accuracy
        self._top_left_width = top_left_width
        self._top_left_height = top_left_height
        self._top_right_width = top_right_width
        self._bottom_right_height = bottom_right_height

    def __repr__(self) -> str:
        return (
            f"Display: {self._display} "
            f"Menu Accuracy: {self._menu_accuracy} "
            f"News Accuracy: {self._news_accuracy} "
            f"Home Accuracy: {self._home_accuracy} "
            f"Aspect Ratio: {self._aspect_ratio}"
        )

    def __iter__(self):
        yield self._menu_accuracy
        yield self._news_accuracy
        yield self._home_accuracy

    def game_area(self) -> dict:
        return {
            "top": self._aspect_ratio["top"] + self._top_left_height,
            "left": self._aspect_ratio["left"] + self._top_left_width,
            "width": self._aspect_ratio["width"]
            - (self._aspect_ratio["width"] - self._top_right_width)
            - self._top_left_width,
            "height": self._aspect_ratio["height"]
            - (self._aspect_ratio["height"] - self._bottom_right_height)
            - self._top_left_height,
            "mon": self._display,
        }


if __name__ == "__main__":

    args = parse.parse_args()

    template_image_menu = cv.imread(args.menu, cv.IMREAD_UNCHANGED)

    template_image_news = cv.imread(args.news, cv.IMREAD_UNCHANGED)

    template_image_home = cv.imread(args.home, cv.IMREAD_UNCHANGED)

    w_menu, h_menu = template_image_menu.shape[::-1]
    w_news, h_news = template_image_news.shape[::-1]
    w_home, h_home = template_image_home.shape[::-1]
    
    with mss.mss() as sct:
        while True:
            last_time = time.time()

            search = []

            for index, monitor in enumerate(sct.monitors[2:]):
                screenshot = np.array(sct.grab(monitor))

                screenshot = cv.cvtColor(screenshot, cv.COLOR_RGBA2GRAY)


                res_menu = cv.matchTemplate(
                    template_image_menu, screenshot, cv.TM_SQDIFF_NORMED
                )

                res_news = cv.matchTemplate(
                    template_image_news, screenshot, cv.TM_SQDIFF_NORMED
                )

                res_home = cv.matchTemplate(
                    template_image_home, screenshot, cv.TM_SQDIFF_NORMED
                )

                # For SQDIFF and SQDIFF_NORMED, the best matches are lower values. For all the other methods, the higher the better
                min_val_menu, _, min_loc_menu, _ = cv.minMaxLoc(res_menu)
                min_val_news, _, min_loc_news, _ = cv.minMaxLoc(res_news)
                min_val_home, _, min_loc_home, _ = cv.minMaxLoc(res_home)

                search.append(
                    CalibrationScreen(
                        display=(index + 1),
                        aspect_ratio=monitor,
                        menu_accuracy=(1 - min_val_menu),
                        news_accuracy=(1 - min_val_news),
                        home_accuracy=(1 - min_val_home),
                        top_left_width=(min_loc_news[0]),
                        top_left_height=(min_loc_news[1]),
                        top_right_width=(min_loc_menu[0] + w_menu),
                        bottom_right_height=(min_loc_home[1] + h_home),
                    )
                )

            result = max(
                search,
                key=lambda screen: screen._menu_accuracy
                + screen._news_accuracy
                + screen._home_accuracy,
            )

            sct_img = sct.grab(result.game_area())

            img_show = np.array(sct_img)

            cv.imshow("", cv.cvtColor(img_show, cv.COLOR_RGBA2GRAY))

            print(f"fps: {1 / (time.time() - last_time)}")

            if cv.waitKey(25) & 0xFF == ord("q"):
                cv.destroyAllWindows
                break
