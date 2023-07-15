import numpy as np
import cv2 as cv
import pyautogui
from PIL import Image
from PIL import ImageGrab
from pyscreeze import screenshot


def start():
    # image = pyautogui.screenshot()

    # image = cv.cvtColor(np.array(image),
    # cv.COLOR_RGB2BGR)

    screenshot = ImageGrab.grab(
        bbox=None, include_layered_windows=False, all_screens=False
    )

    screenshot.show()

    # im = Image.open(image)

    # im.show()

    # cv.imshow('Teste SS', image)
    #
    # cv.waitKey(0)
    #
    # cv.destroyAllWindows()
