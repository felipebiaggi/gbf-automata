import cv2 as cv
from pathlib import Path
from gbf_automata.enums.template_match import TemplateMatch
from gbf_automata.models.image import ImageModel

resource_dir = Path(__file__).parent.parent / "resources"

template_path = resource_dir / "template_image_gray.png"
target_path = resource_dir / "target_image.png"


if __name__ == "__main__":

    target_rgb = cv.imread(target_path.as_posix())

    target_gray = cv.cvtColor(target_rgb, cv.COLOR_BGR2GRAY)

    template = cv.imread(template_path.as_posix(), cv.IMREAD_UNCHANGED)

    target_source = target_rgb.copy()

    w, h = template.shape[::-1]

    method = TemplateMatch.TM_CCORR_NORMED

    res = cv.matchTemplate(target_gray, template, method)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    image_area = ImageModel(
        method=method,
        image_width=w,
        image_height=h,
        min_val=min_val,
        max_val=max_val,
        min_loc=min_loc,
        max_loc=max_loc,
    )

    top_left, bottom_right = image_area.plot_area()

    cv.namedWindow("Souce", cv.WINDOW_KEEPRATIO)
    cv.rectangle(target_source, top_left, bottom_right, (0, 0, 255), 4)
    cv.imshow("Souce", target_source)
    cv.waitKey(0)
