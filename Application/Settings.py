from dataclasses import dataclass, field
from enum import Enum
from typing import Dict


@dataclass(frozen=True)
class MainWindowSettings:
    """
    TODO: document MainWindowSettings and members
    """

    zoomMinimumValue: float = 0.0
    zoomMaximumValue: float = 20.0
    zoomSingleStep: float = 0.05
    zoomPageStep: float = 1.0
    zoomDefaultValue: float = 1.0
    ticksInterval: int = 1

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

    frameGridSize: int = 9  # positive odd number here
    threeZoneHeightPadding: int = 12  # in pixels
    fourZoneHeightPadding: int = 6  # in pixels
    fontSize: int = 8  # in points

    class ColorSpaces(Enum):
        RGB = (0, 'RGB (Red, Green, Blue) (max. 255R, 255G, 255B)')
        HSL = (1, 'HSL (Hue, Saturation, Lightness) (max. 359°, 100%, 100%)')
        HSV = (2, 'HSV (Hue, Saturation, Value) (max. 359°, 100%, 100%)')
        CMYK = (3, 'CMYK (Cyan, Magenta, Yellow, Black) (max. 100%, 100%, 100%, 100%)')
        GRAY = (4, 'Grayscale (max. 255G)')

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


@dataclass(frozen=True)
class RightClickPointerSettings:
    """
        TODO: document RightClickPointerSettings
    """

    aroundClickSquareSize: int = 9  # in pixels
    numberOfClicksToRemember = 4
