def relativeColorLuminance(QColor):
    """
    TODO: document calculateColorLuminance
    :param QColor:
    :return:
    """
    componentsList = [QColor.red(), QColor.green(), QColor.blue()]

    # sRGB to linear RGB conversion with gamma correction
    # it's safe to assume that everything on a PC is in the sRGB color space
    # https://stackoverflow.com/a/3943023

    # https://en.wikipedia.org/wiki/SRGB#The_reverse_transformation
    for componentIndex in range(3):
        component = componentsList[componentIndex] / 255
        if component <= 0.04045:
            component /= 12.92
        else:
            component = ((component + 0.055) / 1.055) ** 2.4

        componentsList[componentIndex] = component

    # https://en.wikipedia.org/wiki/Luma_%28video%29#Use_of_relative_luminance
    return 0.2126 * componentsList[0] + 0.7152 * componentsList[1] + 0.0722 * componentsList[2]

def calculateContrastRatio(QColor1, QColor2):
    """
    TODO: document calculateContrastRatio
    Calculates contrast ratio according to WCAG 2.0 formula
    Will return a value between 1 (no contrast) and 21 (max contrast)
    https://www.w3.org/TR/WCAG20/#contrast-ratiodef
    :param QColor:
    :return:
    """
    luminanceColor1 = relativeColorLuminance(QColor1)
    luminanceColor2 = relativeColorLuminance(QColor2)

    # the first luminance has to be the lightest, so the biggest
    if luminanceColor1 < luminanceColor2:
        luminanceColor1, luminanceColor2 = luminanceColor2, luminanceColor1

    return (luminanceColor1 + 0.05) / (luminanceColor2 + 0.05)


def greatestContrastTextColorForBackground(QColorText1, QColorText2, QColorBackground):
    """
    TODO: document greatestContrastTextColorForBackground
    Compares two text colors and returns the one with the greatest contrast relative to the background.
    :param QColor:
    :return:
    """
    contrastRatio1 = calculateContrastRatio(QColorText1, QColorBackground)
    contrastRatio2 = calculateContrastRatio(QColorText2, QColorBackground)

    if contrastRatio1 > contrastRatio2:
        return QColorText1
    else:
        return QColorText2
