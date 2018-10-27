from enum import Enum


class MainWindowSettings:

    @property
    def zoomMinimumValue(self):
        """
        TODO: document MainWindowSettings.zoomMinimumValue
        :return:
        """
        return 0.0

    @property
    def zoomMaximumValue(self):
        """
        TODO: document MainWindowSettings.zoomMaximumValue
        :return:
        """
        return 20.0

    @property
    def zoomSingleStep(self):
        """
        TODO: document MainWindowSettings.zoomSingleStep
        :return:
        """
        return 0.05

    @property
    def zoomPageStep(self):
        """
        TODO: document MainWindowSettings.zoomPageStep
        :return:
        """
        return 1.0

    @property
    def zoomDefaultValue(self):
        """
        TODO: document MainWindowSettings.zoomDefaultValue
        :return:
        """
        return 1.0

    @property
    def ticksInterval(self):
        """
        TODO: document MainWindowSettings.ticksInterval
        :return:
        """
        return 1


# had to make it singleton so that the properties might call themselves correctly
MainWindowSettings = MainWindowSettings()


class MagnifierWindowSettings:

    @property
    def frameGridSize(self):
        return 9

    @frameGridSize.getter
    def frameGridSize(self):
        """
        TODO document MagnifierWindowSettings.frameGridSize
        :return:
        """
        return 9  # positive odd number here

    @property
    def threeZoneHeightPadding(self):
        """
        TODO document MagnifierWindowSettings.threeZoneHeightPadding
        :return:
        """
        return 12  # in pixels

    @property
    def fourZoneHeightPadding(self):
        """
        TODO document MagnifierWindowSettings.fourZoneHeightPadding
        :return:
        """
        return 6  # in pixels

    @property
    def fontSize(self):
        """
        TODO document MagnifierWindowSettings.fontSize
        :return:
        """
        return 8  # in points

    class ColorSpaces(Enum):
        RGB = (0, 'RGB (Red Green Blue)')
        HSL = (1, 'HSL (Hue Saturation Lightness)')
        HSV = (2, 'HSV (Hue Saturation Value)')
        CMYK = (3, 'CMYK (Cyan Magenta Yellow Black)')
        GRAY = (4, 'Grayscale')


# had to make it singleton so that the properties might call themselves correctly
MagnifierWindowSettings = MagnifierWindowSettings()


class PlotterWindowSettings:
    class Functions(Enum):
        PLOT_ROW_VALUES = (0, 'Plot row values')
        PLOT_COL_VALUES = (1, 'Plot column values')
        PLOT_HISTOGRAM = (2, 'Plot histogram')
