from PyQt5 import QtCore, QtGui, QtWidgets
import cv2 as opencv
import Application.Settings


class MainWindowImageLabel(QtWidgets.QLabel):
    mouse_moved = QtCore.pyqtSignal(QtGui.QMouseEvent, name='mouseMoved')
    mouse_pressed = QtCore.pyqtSignal(QtGui.QMouseEvent, name='mousePressed')
    mouse_leaved = QtCore.pyqtSignal(QtCore.QEvent, name='mouseLeaved')
    finished_painting = QtCore.pyqtSignal(name='finishedPainting')

    def __init__(self, parent=None):
        super().__init__(parent)
        self._qImage = None
        self._zoom = 1.0
        self._clickPosition = None

    def setZoom(self, zoom):
        self._zoom = zoom
        if self._qImage is not None:
            self.setFixedSize(self._qImage.size() * zoom)

    def mouseMoveEvent(self, QMouseEvent):
        self.mouse_moved.emit(QMouseEvent)

    def mousePressEvent(self, QMouseEvent):
        self.mouse_pressed.emit(QMouseEvent)

    def leaveEvent(self, QEvent):
        self.mouse_leaved.emit(QEvent)

    def setClickPosition(self, clickPosition: QtCore.QPoint):
        self._clickPosition = clickPosition
        self.update()

    def setLabelImage(self, image):
        # TODO: think about moving this to VM
        if image is not None:
            if len(image.shape) == 3:
                self._qImage = QtGui.QImage(opencv.cvtColor(image, opencv.COLOR_BGR2RGB).data,
                                             image.shape[1],
                                             image.shape[0],
                                             3 * image.shape[1],
                                             QtGui.QImage.Format_RGB888)
            elif len(image.shape) == 2:
                self._qImage = QtGui.QImage(image.data,
                                             image.shape[1],
                                             image.shape[0],
                                             image.shape[1],
                                             QtGui.QImage.Format_Grayscale8)

            self.setFixedSize(self._qImage.size())
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
            painter.setPen(QtGui.QPen(QtCore.Qt.red))
            painter.pen().setWidth(1)

            if self._clickPosition is not None:
                cornerCalcOffset = int(Application.Settings.MagnifierWindowSettings.frameGridSize / 2) + 1

                # vertical line
                painter.drawLine(self._clickPosition.x(), 0, self._clickPosition.x(), (self.height() - 1) // self._zoom )

                # horizontal line
                painter.drawLine(0, self._clickPosition.y(), (self.width() - 1) // self._zoom, self._clickPosition.y())

                # +1 because we need to take into account the thickness of the rectangle itself
                # we want its contents inside to be frameGridSize^2
                painter.drawRect(self._clickPosition.x() - cornerCalcOffset,
                                 self._clickPosition.y() - cornerCalcOffset,
                                 Application.Settings.MagnifierWindowSettings.frameGridSize + 1,
                                 Application.Settings.MagnifierWindowSettings.frameGridSize + 1)


        self.finished_painting.emit()