from PyQt5 import QtCore, QtGui, QtWidgets

from Application.Settings import MagnifierWindowSettings
import Application.Utils.ColorSpaceOperations


class MagnifierPixelFrame(QtWidgets.QFrame):
    """
    TODO: document MagnifierPixelFrame
    """

    def __init__(self, parent=None):
        """
        TODO: document MagnifierPixelFrame constructor
        """
        super().__init__(parent)
        self._isVisible = False
        self._backgroundColor = QtGui.QColor(255, 255, 255)
        self._colorDisplayFormat = MagnifierWindowSettings.ColorSpaces.RGB

    def setColorDisplayFormat(self, colorSpace: MagnifierWindowSettings.ColorSpaces):
        """
        TODO: document MagnifierPixelFrame.setColorDisplayFormat
        """
        self._colorDisplayFormat = colorSpace
        self.update()

    def setFrameColorRgb(self, red, green, blue):
        """
        TODO: document MagnifierPixelFrame.setFrameColorRgb
        """
        if red is not None and green is not None and blue is not None:
            self._isVisible = True
            self._backgroundColor = QtGui.QColor(red, green, blue)
        else:
            self.clear()

        self.update()

    def setFrameColorGrayLevel(self, grayLevel):
        """
        TODO: document MagnifierPixelFrame.setFrameColorGrayLevel
        """
        self.setFrameColorRgb(grayLevel, grayLevel, grayLevel)

    def clear(self):
        """
        TODO: document MagnifierPixelFrame.clear
        """
        self._isVisible = False
        self._backgroundColor = QtGui.QColor(255, 255, 255)

    def paintEvent(self, QPaintEvent):
        """
        TODO: document MagnifierPixelFrame.paintEvent
        """

        # TODO: spart in functii maybe? pt a fi mai lizibil
        if self._isVisible:
            painter = QtGui.QPainter(self)
            painter.fillRect(self.rect(), self._backgroundColor)

            font = QtGui.QFont("Arial")
            font.setPointSize(MagnifierWindowSettings.fontSize)
            painter.setFont(font)
            fontMetrics = QtGui.QFontMetrics(font)

            if Application.Utils.ColorSpaceOperations.isColorDark(self._backgroundColor):
                painter.setPen(QtCore.Qt.white)
            else:
                painter.setBrush(QtCore.Qt.black)

            if self._colorDisplayFormat is MagnifierWindowSettings.ColorSpaces.GRAY:
                text = str((self._backgroundColor.red() + self._backgroundColor.green() +
                            self._backgroundColor.blue()) // 3)

                horizontalAdvance = fontMetrics.horizontalAdvance(text, len(text))

                painter.drawText((self.width() - horizontalAdvance) / 2,
                                 self.height() / 2 + fontMetrics.ascent() / 2,
                                 text)
            elif self._colorDisplayFormat is MagnifierWindowSettings.ColorSpaces.CMYK:
                textCyan = str(self._backgroundColor.cyan())
                textMagenta = str(self._backgroundColor.magenta())
                textYellow = str(self._backgroundColor.yellow())
                textBlack = str(self._backgroundColor.black())

                horizontalAdvanceCyan = fontMetrics.horizontalAdvance(textCyan, len(textCyan))
                horizontalAdvanceMagenta = fontMetrics.horizontalAdvance(textMagenta, len(textMagenta))
                horizontalAdvanceYellow = fontMetrics.horizontalAdvance(textYellow, len(textYellow))
                horizontalAdvanceBlack = fontMetrics.horizontalAdvance(textBlack, len(textBlack))

                # the frame is split into equal rectangles called zones
                # this tries to center the text in one of the 3 zones of the frame
                # the (usually) visible part of the text is the ascent, not the height
                # fonts usually have a baseline; the font will have parts of it below the baseline
                # but those are exceptions (eg. Q - the line below the O that forms the Q is below the baseline)
                zoneHeight = (self.height() - MagnifierWindowSettings.fourZoneHeightPadding) / 4
                halfFontAscent = fontMetrics.ascent() / 2
                halfZoneHeight = zoneHeight / 2
                zoneHeightOffset = halfZoneHeight - halfFontAscent - MagnifierWindowSettings.fourZoneHeightPadding / 2

                painter.drawText((self.width() - horizontalAdvanceCyan) / 2, zoneHeight - zoneHeightOffset,
                                 textCyan)
                painter.drawText((self.width() - horizontalAdvanceMagenta) / 2, zoneHeight * 2 - zoneHeightOffset,
                                 textMagenta)
                painter.drawText((self.width() - horizontalAdvanceYellow) / 2, zoneHeight * 3 - zoneHeightOffset,
                                 textYellow)
                painter.drawText((self.width() - horizontalAdvanceBlack) / 2, zoneHeight * 4 - zoneHeightOffset,
                                 textBlack)
            else:
                if self._colorDisplayFormat is MagnifierWindowSettings.ColorSpaces.RGB:
                    textFirst = str(self._backgroundColor.red())
                    textSecond = str(self._backgroundColor.green())
                    textThird = str(self._backgroundColor.blue())
                elif self._colorDisplayFormat is MagnifierWindowSettings.ColorSpaces.HSL:
                    textFirst = str(self._backgroundColor.hue())
                    textSecond = str(self._backgroundColor.saturation())
                    textThird = str(self._backgroundColor.lightness())
                elif self._colorDisplayFormat is MagnifierWindowSettings.ColorSpaces.HSV:
                    textFirst = str(self._backgroundColor.hue())
                    textSecond = str(self._backgroundColor.saturation())
                    textThird = str(self._backgroundColor.value())

                horizontalAdvanceRed = fontMetrics.horizontalAdvance(textFirst, len(textFirst))
                horizontalAdvanceGreen = fontMetrics.horizontalAdvance(textSecond, len(textSecond))
                horizontalAdvanceBlue = fontMetrics.horizontalAdvance(textThird, len(textThird))

                # the frame is split into equal rectangles called zones
                # this tries to center the text in one of the 3 zones of the frame
                # the (usually) visible part of the text is the ascent, not the height
                # fonts usually have a baseline; the font will have parts of it below the baseline
                # but those are exceptions (eg. Q - the line below the O that forms the Q is below the baseline)
                zoneHeight = (self.height() - MagnifierWindowSettings.threeZoneHeightPadding) / 3
                halfFontAscent = fontMetrics.ascent() / 2
                halfZoneHeight = zoneHeight / 2
                zoneHeightOffset = halfZoneHeight - halfFontAscent - MagnifierWindowSettings.threeZoneHeightPadding / 2

                painter.drawText((self.width() - horizontalAdvanceRed) / 2, zoneHeight - zoneHeightOffset,
                                 textFirst)
                painter.drawText((self.width() - horizontalAdvanceGreen) / 2, zoneHeight * 2 - zoneHeightOffset,
                                 textSecond)
                painter.drawText((self.width() - horizontalAdvanceBlue) / 2, zoneHeight * 3 - zoneHeightOffset,
                                 textThird)