from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(frozen=True)
class MainWindowSettings:
    """
    TODO: document MainWindowSettings and members
    """

    zoomMinimumValue: float = field(default=0.0, init=False)
    zoomMaximumValue: float = field(default=20.0, init=False)
    zoomSingleStep: float = field(default=0.05, init=False)
    zoomPageStep: float = field(default=1.0, init=False)
    zoomDefaultValue: float = field(default=1.0, init=False)
    ticksInterval: int = field(default=1, init=False)

    def __post_init__(self):
        # TODO: think if more tests are needed
        assert self.zoomMinimumValue < self.zoomMaximumValue
        assert self.zoomMinimumValue < self.zoomDefaultValue < self.zoomMaximumValue


@dataclass()
class MagnifierWindowSettings:
    """
    TODO: document MagnifierWindowSettings
    """

    class ColorSpaces(Enum):
        RGB = (0, 'RGB (Red Green Blue)')
        HSL = (1, 'HSL (Hue Saturation Lightness)')
        HSV = (2, 'HSV (Hue Saturation Value)')
        CMYK = (3, 'CMYK (Cyan Magenta Yellow Black)')
        GRAY = (4, 'Grayscale')

    aa: Any

    frameGridSize: int = field(default=9, init=False)  # positive odd number here
    threeZoneHeightPadding: int = field(default=12, init=False)  # in pixels
    fourZoneHeightPadding: int = field(default=6, init=False)  # in pixels
    fontSize: int = field(default=8, init=False)  # in points

    def __post_init__(self):
        # TODO: think if more tests are needed
        assert self.frameGridSize % 2 == 1
        assert self.frameGridSize > 0
        assert self.fontSize > 0


# TODO: to be removed and replaced by functions defined in PlotterAlgorithms folder
class PlotterWindowSettings:
    class Functions(Enum):
        PLOT_ROW_VALUES = (0, 'Plot row values')
        PLOT_COL_VALUES = (1, 'Plot column values')
        PLOT_HISTOGRAM = (2, 'Plot histogram')
