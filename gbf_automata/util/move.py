import cv2 as cv
import mss
import numpy as np
import pyautogui

from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.exception.gbf_automata_exception import GBFAutomataError
from gbf_automata.models.image import ImageModel


def move(
    element: str,
    accuracy_threshold: float = 0.90,
    method: TemplateMatch = TemplateMatch.TM_CCOEFF_NORMED,
) -> None:
    template = cv.imread(element, cv.IMREAD_UNCHANGED)

    template_height, template_width = template.shape

    with mss.mss() as sct:
        monitor = sct.monitors[0]

        target_image = cv.cvtColor(
            src=np.asarray(sct.grab(monitor)), code=cv.COLOR_RGBA2GRAY
        )

        res_image = cv.matchTemplate(target_image, template, method)

        min_val_image, max_val_image, min_loc_image, max_loc_image = cv.minMaxLoc(
            res_image
        )

        image_model = ImageModel(
            method=method,
            template_height=template_height,
            template_width=template_width,
            min_loc=min_loc_image,
            max_loc=max_loc_image,
            min_val=min_val_image,
            max_val=max_val_image,
        )

        accuracy = image_model.accuracy()

        if accuracy < accuracy_threshold:
            raise GBFAutomataError(
                f"Accuracy Error - Threshold: <{accuracy_threshold}> - Mensured: <{accuracy}> - Element: <{element}>"
            )

        pyautogui.moveTo(*image_model.center())

        pyautogui.click()
