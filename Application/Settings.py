from enum import Enum

class MagnifierWindowSettings:
    frameGridSize = 9

class PlotterWindowSettings:
    class Functions(Enum):
        PLOT_ROW_GRAY_VALUES = 'Plot row gray values'
        PLOT_COL_GRAY_VALUES = 'Plot column gray values'
