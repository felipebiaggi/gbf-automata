import mss
import cv2 as cv
import numpy as np
from typing import List, Tuple
from gbf_automata.classes import default
from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.schema.image_schema import ImageModel
from gbf_automata.classes.default import Default
from gbf_automata.exception.gbf_automata_exception import GBFAutomataError
from gbf_automata.util.settings import settings
from gbf_automata.util.logger import get_logger


logger = get_logger(__name__)

method = TemplateMatch.TM_CCOEFF_NORMED
correction = (0, 0)


def create_image_model(image_path: str, default: Default):
    img = cv.imread(image_path, cv.IMREAD_UNCHANGED)

    w_img, h_img = img.shape[::-1]

    with mss.mss() as sct:
        template = cv.cvtColor(
            src=np.asarray(sct.grab(default.game_area())), code=cv.COLOR_RGB2GRAY
        )

        res_image = cv.matchTemplate(image=img, templ=template, method=method)

        (min_val_image, max_val_image, min_loc_image, max_loc_image) = cv.minMaxLoc(
            res_image
        )

        return ImageModel(
            image_width=w_img,
            image_height=h_img,
            min_val=min_val_image,
            max_val=max_val_image,
            min_loc=min_loc_image,
            max_loc=max_loc_image,
            method=method,
            correction=correction,
        )


def default_area():
    image_menu = cv.imread(settings.image_menu, cv.IMREAD_UNCHANGED)
    image_home_default = cv.imread(settings.image_home_default, cv.IMREAD_UNCHANGED)
    image_home = cv.imread(settings.image_home, cv.IMREAD_UNCHANGED)

    w_menu, h_menu = image_menu.shape[::-1]
    w_home_default, h_home_default = image_home_default.shape[::-1]
    w_home, h_home = image_home.shape[::-1]

    search: List = []

    with mss.mss() as sct:
        with mss.mss() as sct:
            for index, monitor in enumerate(sct.monitors):
                display_template = np.asarray(sct.grab(monitor))

                display_template = cv.cvtColor(
                    src=display_template, code=cv.COLOR_RGBA2GRAY
                )

                res_menu = cv.matchTemplate(
                    image=image_menu, templ=display_template, method=method
                )

                res_home_default = cv.matchTemplate(
                    image=image_home_default, templ=display_template, method=method
                )

                res_home = cv.matchTemplate(
                    image=image_home, templ=display_template, method=method
                )

                min_val_menu, max_val_menu, min_loc_menu, max_loc_menu = cv.minMaxLoc(
                    res_menu
                )

                (
                    min_val_home_default,
                    max_val_home_default,
                    min_loc_home_default,
                    max_loc_home_default,
                ) = cv.minMaxLoc(res_home_default)

                min_val_home, max_val_home, min_loc_home, max_loc_home = cv.minMaxLoc(
                    res_home
                )

                if method in [TemplateMatch.TM_SQDIFF_NORMED, TemplateMatch.TM_SQDIFF]:
                    correction = min_loc_home_default
                else:
                    correction = max_loc_home_default

                menu_model = ImageModel(
                    method=method,
                    image_width=w_menu,
                    image_height=h_menu,
                    min_val=min_val_menu,
                    max_val=max_val_menu,
                    min_loc=min_loc_menu,
                    max_loc=max_loc_menu,
                    correction=correction,
                )

                home_default_model = ImageModel(
                    method=method,
                    image_width=w_home_default,
                    image_height=h_home_default,
                    min_val=min_val_home_default,
                    max_val=max_val_home_default,
                    min_loc=min_loc_home_default,
                    max_loc=max_loc_home_default,
                    correction=correction,
                )

                home_model = ImageModel(
                    method=method,
                    image_width=w_home,
                    image_height=h_home,
                    min_val=min_val_home,
                    max_val=max_val_home,
                    min_loc=min_loc_home,
                    max_loc=max_loc_home,
                    correction=correction,
                )

                logger.debug(f"Model Home Top <{home_default_model}>")
                logger.debug(f"Model Menu Default <{menu_model}>")
                logger.debug(f"Model Home Bottom <{home_model}>")

                search.append(
                    Default(
                        aspect_ratio=monitor,
                        menu=menu_model,
                        top_left_home=home_default_model,
                        bottom_right_home=home_model,
                    )
                )

    return max(search, key=lambda game_area: game_area.accuracy())


def draw_element(image, top_left: Tuple[int, int], bottom_right: Tuple[int, int]):
    cv.rectangle(image, top_left, bottom_right, (0, 0, 255), 2)


def render(default: Default, image_model_list: List[ImageModel]):
    while True:
        with mss.mss() as sct:
            img = sct.grab(default.game_area())

            np_image = np.asarray(img)

            for model in image_model_list:
                top_left, bottom_right = model.plot_area()

                draw_element(
                    image=np_image, top_left=top_left, bottom_right=bottom_right
                )

        cv.imshow("", np_image)

        if cv.waitKey(25) & 0xFF == ord("q"):
            cv.destroyAllWindows
            break


if __name__ == "__main__":
    image_list = [
        settings.image_zone_mundus,
        settings.image_zone_eletio,
        settings.image_zone_faym,
        settings.image_zone_goliath,
        settings.image_zone_harbinger,
        settings.image_zone_invidia,
        settings.image_zone_joculator,
        settings.image_zone_kalendae,
        settings.image_zone_liber,
    ]

    image_model_list = []

    default_area: Default = default_area()

    for element, accuracy in default_area.accuracy():
        if accuracy < 0.95:
            raise GBFAutomataError(
                f"Low in element: <{element}> | accuracy <{accuracy}>"
            )

    logger.info(f"Game Area: <{default_area.game_area()}>")

    for image in image_list:
        image_model_list.append(
            create_image_model(image_path=image, default=default_area)
        )

    render(default=default_area, image_model_list=image_model_list)
