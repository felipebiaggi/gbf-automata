import cv2 as cv
import mss
import numpy as np

from gbf_automata.enums.game_states import GameStates
from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.exception.gbf_automata_exception import GBFAutomataError
from gbf_automata.models.data import get_data
from gbf_automata.models.game_area import GameArea
from gbf_automata.models.image import ImageModel

data_model = get_data()


def calibrate(game_state: GameStates, accuracy_threshold: float = 0.90) -> GameArea:
    method = TemplateMatch.TM_CCOEFF_NORMED

    if game_state == GameStates.START:
        template_top = cv.imread(data_model.main.news, cv.IMREAD_UNCHANGED)
    else:
        template_top = cv.imread(data_model.main.home_top, cv.IMREAD_UNCHANGED)

    template_bottom = cv.imread(data_model.main.home_bottom, cv.IMREAD_UNCHANGED)

    height_top, width_top = template_top.shape

    height_bottom, width_bottom = template_bottom.shape

    with mss.mss() as sct:
        monitor = sct.monitors[0]

        target_image = cv.cvtColor(
            src=np.asarray(sct.grab(monitor)), code=cv.COLOR_RGBA2GRAY
        )

        res_image_top = cv.matchTemplate(target_image, template_top, method)

        res_image_bottom = cv.matchTemplate(target_image, template_bottom, method)

        min_val_top, max_val_top, min_loc_top, max_loc_top = cv.minMaxLoc(res_image_top)

        min_val_bottom, max_val_bottom, min_loc_bottom, max_loc_bottom = cv.minMaxLoc(
            res_image_bottom
        )

        top = ImageModel(
            method=method,
            template_width=width_top,
            template_height=height_top,
            min_val=min_val_top,
            max_val=max_val_top,
            min_loc=min_loc_top,
            max_loc=max_loc_top,
        )

        bottom = ImageModel(
            method=method,
            template_width=width_bottom,
            template_height=height_bottom,
            min_val=min_val_bottom,
            max_val=max_val_bottom,
            min_loc=min_loc_bottom,
            max_loc=max_loc_bottom,
        )

        game_area = GameArea(top_left=top, bottom_right=bottom, aspect_ratio=monitor)

        for name, accuracy in game_area.accuracy():
            if accuracy < accuracy_threshold:
                raise GBFAutomataError(
                    f"Accuracy Error - Threshold: <{accuracy_threshold}> - Mensured: <{accuracy}> - Element: <{name}>"
                )

        return game_area
