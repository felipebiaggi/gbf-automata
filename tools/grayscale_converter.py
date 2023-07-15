import argparse
import cv2 as cv
from pathvalidate.argparse import sanitize_filepath_arg, sanitize_filename_arg

parse = argparse.ArgumentParser(
    prog="Grayscale generator", description="Converter an image to grayscale"
)
parse.add_argument("-f", "--filepath", type=sanitize_filepath_arg)

parse.add_argument("-n", "--name", type=sanitize_filename_arg)

parse.add_argument("-o", "--output", type=sanitize_filepath_arg)

if __name__ == "__main__":
    args = parse.parse_args()

    img = cv.imread(args.filepath, cv.IMREAD_GRAYSCALE)

    status = cv.imwrite(f"{args.output}/{args.name}_gray.png", img)
