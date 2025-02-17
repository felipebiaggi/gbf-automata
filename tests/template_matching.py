import cv2 as cv
from pathlib import Path
from gbf_automata.models.image import ImageModel
from gbf_automata.enums.template_match import TemplateMatch

resource_dir = Path(__file__).parent.parent / "resources"

template_path = resource_dir / "template_image_gray.png"
target_path = resource_dir / "target_image.png"


if __name__ == "__main__":
    target_rgb = cv.imread(target_path.as_posix())

    target_gray = cv.cvtColor(target_rgb, cv.COLOR_BGR2GRAY)

    template = cv.imread(template_path.as_posix(), cv.IMREAD_UNCHANGED)

    target_source = target_rgb.copy()

    template_h, template_w = template.shape

    method = TemplateMatch.TM_CCORR_NORMED

    res = cv.matchTemplate(target_gray, template, method)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    image_area = ImageModel(
        method=method,
        template_width=template_w,
        template_height=template_h,
        min_val=min_val,
        max_val=max_val,
        min_loc=min_loc,
        max_loc=max_loc,
    )

    top_left, bottom_right = image_area.plot_area()

    cv.namedWindow("Target", cv.WINDOW_KEEPRATIO)
    cv.rectangle(target_source, top_left, bottom_right, (0, 0, 255), 4)
    cv.imshow("Target", target_source)

    while cv.getWindowProperty("Target", cv.WND_PROP_VISIBLE) >= 1:
        key = cv.waitKey(1000)
        if key == 27:
            break

    cv.destroyAllWindows()
