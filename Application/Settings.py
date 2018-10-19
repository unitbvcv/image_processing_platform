from enum import Enum


class MagnifierWindowSettings:
    frameGridSize = 9  # positive odd number here
    threeZoneHeightPadding = 12  # in pixels
    fourZoneHeightPadding = 6  # in pixels
    fontSize = 8  # in points

    class ColorSpaces(Enum):
        RGB = (0, 'RGB (Red Green Blue)')
        HSL = (1, 'HSL (Hue Saturation Lightness)')
        HSV = (2, 'HSV (Hue Saturation Value)')
        CMYK = (3, 'CMYK (Cyan Magenta Yellow Black)')
        GRAY = (4, 'Grayscale')


class PlotterWindowSettings:
    class Functions(Enum):
        PLOT_ROW_GRAY_VALUES = (0, 'Plot row gray values')
        PLOT_COL_GRAY_VALUES = (1, 'Plot column gray values')
