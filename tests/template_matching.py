import argparse
import cv2 as cv
from pathvalidate.argparse import sanitize_filepath_arg
from matplotlib import pyplot as plt

parse = argparse.ArgumentParser(
    prog="Template matching",
    description="Find objects in an image using template matching method",
)
parse.add_argument("-i", "--image", type=sanitize_filepath_arg)
parse.add_argument("-t", "--template", type=sanitize_filepath_arg)

if __name__ == "__main__":
    args = parse.parse_args()

    image_rgb = cv.imread(args.image)

    image_gray = cv.cvtColor(image_rgb, cv.COLOR_BGR2GRAY)

    template = cv.imread(args.template, cv.IMREAD_UNCHANGED)

    w, h = template.shape[::-1]

    print(w)
    print(h)

    method = cv.TM_SQDIFF

    res = cv.matchTemplate(image_gray, template, method)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    top_left = min_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    print(top_left)
    print(bottom_right)

    cv.rectangle(image_rgb, top_left, bottom_right, (0, 0, 255), 4)

    plt.imshow(cv.cvtColor(image_rgb, cv.COLOR_BGR2RGB))

    plt.show()
