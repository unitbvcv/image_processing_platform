import Application.Settings

def calculateZoomFromSliderValue(value):
    return value * Application.Settings.MainWindowSettings.zoomSingleStep \
           + Application.Settings.MainWindowSettings.zoomMinimumValue

def calculateSliderValueFromZoom(value):
    return int((value - Application.Settings.MainWindowSettings.zoomMinimumValue)
               / Application.Settings.MainWindowSettings.zoomSingleStep)