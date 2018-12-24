from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

import Application.Settings
from collections import deque


class MainWindowImageLabel(QtWidgets.QLabel):
    mouseMovedSignal = pyqtSignal(QtGui.QMouseEvent, name='mouseMovedSignal')
    mousePressedSignal = pyqtSignal(QtGui.QMouseEvent, name='mousePressedSignal')
    mouseLeavedSignal = pyqtSignal(QtCore.QEvent, name='mouseLeavedSignal')
    finishedPaintingSignal = pyqtSignal(name='finishedPaintingSignal')

    @property
    def isImageSet(self):
        return self._qImage is not None

    def __init__(self, parent=None):
        super().__init__(parent)
        self._qImage = None
        self._zoom = Application.Settings.MainWindowSettings.zoomDefaultValue
        self._leftClickPosition = None
        self._rightClickLastPositions = None

    def setZoom(self, zoom):
        self._zoom = zoom
        if self._qImage is not None:
            self.setFixedSize(self._qImage.size() * zoom)

    def setLeftClickPosition(self, clickPosition):
        self._leftClickPosition = clickPosition
        self.update()

    def setRightClickLastPositions(self, rightClickLastPositions: deque):
        self._rightClickLastPositions = rightClickLastPositions
        self.update()

    def mouseMoveEvent(self, QMouseEvent):
        self.mouseMovedSignal.emit(QMouseEvent)

    def mousePressEvent(self, QMouseEvent):
        self.mousePressedSignal.emit(QMouseEvent)

    def leaveEvent(self, QEvent):
        self.mouseLeavedSignal.emit(QEvent)

    def setLabelImage(self, image):
        # TODO: think about moving this to VM
        if image is not None:
            imageShapeLen = len(image.shape)
            if imageShapeLen == 3:
                self._qImage = QtGui.QImage(
                    image.data,  # data
                    image.shape[1],  # width
                    image.shape[0],  # height
                    3 * image.shape[1],  # bytes per line
                    QtGui.QImage.Format_RGB888
                )
            elif imageShapeLen == 2:
                self._qImage = QtGui.QImage(
                    image.data,
                    image.shape[1],
                    image.shape[0],
                    image.shape[1],
                    QtGui.QImage.Format_Grayscale8
                )

            self.setFixedSize(self._qImage.size() * self._zoom)
        else:
            self.setFixedSize(0, 0)
            self._qImage = None

        self.update()

    def paintEvent(self, QPaintEvent):
        if self._qImage is not None:
            painter = QtGui.QPainter(self)

            transform = QtGui.QTransform()
            transform.scale(self._zoom, self._zoom)
            painter.setTransform(transform, False)

            painter.drawImage(0, 0, self._qImage)

            if self._leftClickPosition is not None:
                painter.setPen(QtGui.QPen(QtCore.Qt.red))
                painter.pen().setWidth(1)

                cornerCalcOffset = int(Application.Settings.MagnifierWindowSettings.frameGridSize / 2) + 1

                # vertical line
                painter.drawLine(self._leftClickPosition.x(), 0, self._leftClickPosition.x(), (self.height() - 1) // self._zoom)

                # horizontal line
                painter.drawLine(0, self._leftClickPosition.y(), (self.width() - 1) // self._zoom, self._leftClickPosition.y())

                # +1 because we need to take into account the thickness of the rectangle itself
                # we want its contents inside to be frameGridSize^2
                painter.drawRect(self._leftClickPosition.x() - cornerCalcOffset,
                                 self._leftClickPosition.y() - cornerCalcOffset,
                                 Application.Settings.MagnifierWindowSettings.frameGridSize + 1,
                                 Application.Settings.MagnifierWindowSettings.frameGridSize + 1)

            if self._rightClickLastPositions is not None:
                painter.setPen(QtGui.QPen(QtCore.Qt.blue))
                painter.pen().setWidth(1)

                if Application.Settings.RightClickPointerSettings.showClickOrder:
                    font = QtGui.QFont("Arial")
                    font.setPointSize(Application.Settings.RightClickPointerSettings.clickOrderFontSize)
                    painter.setFont(font)
                    fontMetrics = QtGui.QFontMetrics(font)

                cornerCalcOffset = int(Application.Settings.RightClickPointerSettings.aroundClickSquareSize / 2) + 1

                for clickNumber in range(len(self._rightClickLastPositions)):
                    x, y = self._rightClickLastPositions[clickNumber]

                    # +1 because we need to take into account the thickness of the rectangle itself
                    # we want its contents inside to be frameGridSize^2
                    painter.drawRect(x - cornerCalcOffset,
                                     y - cornerCalcOffset,
                                     Application.Settings.RightClickPointerSettings.aroundClickSquareSize + 1,
                                     Application.Settings.RightClickPointerSettings.aroundClickSquareSize + 1)

                    if Application.Settings.RightClickPointerSettings.showClickOrder:
                        clickNumberStr = str(clickNumber + 1)
                        horizontalAdvance = fontMetrics.horizontalAdvance(clickNumberStr, len(clickNumberStr))

                        painter.drawText(x - horizontalAdvance / 2 + 1,
                                         y + fontMetrics.ascent() / 2 - 1,
                                         clickNumberStr)

        self.finishedPaintingSignal.emit()
