def calculateColorLuminance(QColor):
    componentsList = [QColor.red(), QColor.green(), QColor.blue()]

    # sRGB to linear RGB conversion
    # it's safe to assume that everything on a PC is in the sRGB color space
    # https://stackoverflow.com/a/3943023
    for componentIndex in range(3):
        component = componentsList[componentIndex] / 255
        if component <= 0.03928:
            component /= 12.92
        else:
            component = ((component + 0.055) / 1.055) ** 2.4

        componentsList[componentIndex] = component

    # https://en.wikipedia.org/wiki/Luma_%28video%29#Use_of_relative_luminance
    return 0.2126 * componentsList[0] + 0.7152 * componentsList[1] + 0.0722 * componentsList[2]

def isColorDark(QColor):
    # returns True if the luminance is low enough
    # 0.179 has been calculated using the equations explained here
    # https://stackoverflow.com/a/3943023

    return calculateColorLuminance(QColor) < 0.179
