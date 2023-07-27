from enum import IntEnum


class TemplateMatch(IntEnum):
    TM_SQDIFF = 0
    TM_SQDIFF_NORMED = 1
    TM_CCORR = 2
    TM_CCORR_NORMED = 3
    TM_CCOEFF = 4
    TM_CCOEFF_NORMED = 5
