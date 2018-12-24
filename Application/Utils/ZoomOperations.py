from Application.Settings import MainWindowSettings


def calculateZoomFromSliderValue(value):
    return value * MainWindowSettings.zoomSingleStep + MainWindowSettings.zoomMinimumValue


def calculateSliderValueFromZoom(value):
    return int((value - MainWindowSettings.zoomMinimumValue) / MainWindowSettings.zoomSingleStep)
