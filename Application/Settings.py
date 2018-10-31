from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


@dataclass(frozen=True)
class MainWindowSettings:
    """
    TODO: document MainWindowSettings and members
    """

    zoomMinimumValue: float = field(default=0.0)
    zoomMaximumValue: float = field(default=20.0)
    zoomSingleStep: float = field(default=0.05)
    zoomPageStep: float = field(default=1.0)
    zoomDefaultValue: float = field(default=1.0)
    ticksInterval: int = field(default=1)

    def __post_init__(self):
        # TODO: think if more tests are needed
        assert self.zoomMinimumValue < self.zoomMaximumValue
        assert self.zoomMinimumValue < self.zoomDefaultValue < self.zoomMaximumValue


# TODO: must be singleton; find alternative (tried metaclass, not working) or explain
MainWindowSettings = MainWindowSettings()


@dataclass(frozen=True)
class MagnifierWindowSettings:
    """
    TODO: document MagnifierWindowSettings
    """

    frameGridSize: int = field(default=9)  # positive odd number here
    threeZoneHeightPadding: int = field(default=12)  # in pixels
    fourZoneHeightPadding: int = field(default=6)  # in pixels
    fontSize: int = field(default=8)  # in points

    class ColorSpaces(Enum):
        RGB = (0, 'RGB (Red Green Blue)')
        HSL = (1, 'HSL (Hue Saturation Lightness)')
        HSV = (2, 'HSV (Hue Saturation Value)')
        CMYK = (3, 'CMYK (Cyan Magenta Yellow Black)')
        GRAY = (4, 'Grayscale')

    # TODO: try to find more elegant solution to this
    colorSpacesDict: Dict[int, ColorSpaces] \
        = field(default_factory=lambda:
                {index: colorSp for (index, colorSp) in enumerate(MagnifierWindowSettings.ColorSpaces)})

    def __post_init__(self):
        # TODO: think if more tests are needed
        assert self.frameGridSize % 2 == 1
        assert self.frameGridSize > 0
        assert self.fontSize > 0


# TODO: must be singleton! find alternative or explain
MagnifierWindowSettings = MagnifierWindowSettings()


# TODO: to be removed and replaced by functions defined in PlotterAlgorithms folder
class PlotterWindowSettings:
    class Functions(Enum):
        PLOT_ROW_VALUES = (0, 'Plot row values')
        PLOT_COL_VALUES = (1, 'Plot column values')
        PLOT_HISTOGRAM = (2, 'Plot histogram')
