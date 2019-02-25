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
    zoomTicksInterval: int = 1

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

    gridSize: int = 9  # positive odd number here
    textThreeRowsHeightPadding: int = 12  # in pixels
    textFourRowsHeightPadding: int = 6  # in pixels
    textFontSize: int = 8  # in points

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
        assert self.gridSize % 2 == 1
        assert self.gridSize > 0
        assert self.textFontSize > 0


# TODO: must be singleton! find alternative or explain
MagnifierWindowSettings = MagnifierWindowSettings()


@dataclass(frozen=True)
class RightClickPointerSettings:
    """
        TODO: document RightClickPointerSettings
    """

    aroundClickSquareSize: int = 25  # in pixels
    numberOfClicksToRemember: int = 4
    showClickOrder: bool = True
    clickOrderFontSize: int = 12

    def __post_init__(self):
        # TODO: think if more tests are needed
        assert self.aroundClickSquareSize % 2 == 1
        assert self.numberOfClicksToRemember > 0
        assert self.showClickOrder is bool
        assert self.clickOrderFontSize > 0
