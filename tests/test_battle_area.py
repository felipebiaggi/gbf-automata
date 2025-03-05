from pathlib import Path
from typing import List

import cv2 as cv
import mss
import numpy as np

from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.models.image import ImageModel

raid_dir = Path(__file__).parent.parent / "resources" / "result"

template_attack_buttom_path = raid_dir / "ok_buttom_gray.png"

MATCH_METHOD = TemplateMatch.TM_CCOEFF_NORMED

if __name__ == "__main__":
    template_attack_buttom = cv.imread(
        template_attack_buttom_path.as_posix(), cv.IMREAD_UNCHANGED
    )

    template_attack_buttom_h, template_attack_buttom_w = template_attack_buttom.shape

    with mss.mss() as sct:
        search: List = []

        monitor = sct.monitors[0]
        index = 0
        print(monitor)

        target_image = np.asarray(sct.grab(monitor))

        target_image_gray = cv.cvtColor(src=target_image, code=cv.COLOR_RGBA2GRAY)

        image_source = cv.cvtColor(src=target_image, code=cv.COLOR_RGBA2GRAY)

        res_attack_buttom = cv.matchTemplate(
            target_image_gray, template_attack_buttom, MATCH_METHOD
        )

        min_val_attack, max_val_attack, min_loc_attack, max_loc_attack = cv.minMaxLoc(
            res_attack_buttom
        )

        if MATCH_METHOD in [
            TemplateMatch.TM_SQDIFF_NORMED,
            TemplateMatch.TM_SQDIFF_NORMED,
        ]:
            correction = min_loc_attack
        else:
            correction = max_loc_attack

        attack_model = ImageModel(
            method=MATCH_METHOD,
            template_width=template_attack_buttom_w,
            template_height=template_attack_buttom_h,
            min_val=min_val_attack,
            max_val=max_val_attack,
            min_loc=min_loc_attack,
            max_loc=max_loc_attack,
        )

        search.append(attack_model)

        result: ImageModel = max(search, key=lambda image_model: image_model.accuracy())

        game_area_image = np.asarray(sct.grab(monitor))

        top_left, bottom_right = result.plot_area()

        print(result.accuracy())

        cv.namedWindow("Target:", cv.WINDOW_KEEPRATIO)
        cv.rectangle(game_area_image, top_left, bottom_right, (0, 0, 255), 4)
        cv.imshow("Target", game_area_image)

        while cv.getWindowProperty("Target", cv.WND_PROP_VISIBLE) >= 1:
            key = cv.waitKey(1000)
            if key == 27:
                break

        cv.destroyAllWindows()
