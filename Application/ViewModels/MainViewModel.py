from PyQt5 import QtCore, QtWidgets
from Application.Models import Model
from Application.ViewModels import MagnifierWindowViewModel, PlotterWindowViewModel
# from Application.ViewModels.PlotterWindowViewModel import
import Application.Settings
import numpy as np
import cv2 as opencv


class MainViewModel(QtWidgets.QWidget):
    """
    TODO: document MainViewModel class
    """

    def __init__(self, parent=None):
        """
        # TODO: document MainViewModel constructor
        :param parent:
        """
        super().__init__(parent)

        # Instantiate MainModel
        self._model = Model()

        # Instantiate MagnifierViewModel
        self._magnifierVM = MagnifierWindowViewModel(self)

        # Instantiate PlotterViewModel
        self._plotterVM = PlotterWindowViewModel(self)

        # testing TODO: to remove testing code
        self._magnifierVM.showWindow()

        self._plotterVM.showWindow()

        self._model.originalImage = opencv.imread('C:/Users/vladv/OneDrive/Imagini/WhatsApp Image '
                                                  '2016-10-30 at 20.51.19.jpeg', opencv.IMREAD_GRAYSCALE)
        self.imageClickedEvent(QtCore.QPoint(897, 1590))
        self._magnifierVM.setMagnifierColorSpace(Application.Settings.MagnifierWindowSettings.ColorSpaces.CMYK)
        # self._magnifierVM.resetMagnifier()

    def imageClickedEvent(self, clickPosition):
        """
        # TODO: document MainViewModel.imageClickedEvent
        :param clickPosition: QPoint
        :return:
        """
        if self._magnifierVM.isVisible: # sau plotterul
            # mainWindowVM.highlightPosition(clickPosition)

            magnifiedRegions = self._getMagnifiedRegions(clickPosition)
            self._magnifierVM.setMagnifiedPixels(*magnifiedRegions)

            # set plotter parameters

    def _getMagnifiedRegions(self, clickPosition):
        """
        # TODO: document MainViewModel._getMagnifiedRegions
        :param clickPosition: QPoint
        :return:
        """
        originalImagePixels = self._getMagnifiedRegion(self._model.originalImage, clickPosition)
        processedImagePixels = self._getMagnifiedRegion(self._model.processedImage, clickPosition)
        return originalImagePixels, processedImagePixels

    def _getMagnifiedRegion(self, image, clickPosition):
        """
        # TODO: document MainViewModel._getMagnifiedRegions
        Should explain what the function does here.
        :param clickPosition: QPoint
        :return:
        """
        frameGridSize = Application.Settings.MagnifierWindowSettings.frameGridSize

        imagePixels = np.full((frameGridSize, frameGridSize), None)

        if image is not None:
            if len(image.shape) == 3:
                imagePixels = np.full((frameGridSize, frameGridSize, image.shape[2]), None)

            frameOffset = frameGridSize // 2
            yPos = clickPosition.y()
            xPos = clickPosition.x()

            startIndexes = lambda pos, offset: (pos - offset, 0) if pos - offset >= 0 else (0, offset - pos)
            rowStartIndex, startEmptyRows = startIndexes(yPos, frameOffset)
            columnStartIndex, startEmptyColumns = startIndexes(xPos, frameOffset)

            endIndexes = lambda pos, offset, gridSize, imageSize: \
                (pos + offset + 1, gridSize) if pos + offset + 1 <= imageSize else (imageSize, offset + imageSize - pos)
            rowEndIndex, endFullRows = endIndexes(yPos, frameOffset, frameGridSize, image.shape[0])
            columnEndIndex, endFullColumns = endIndexes(xPos, frameOffset, frameGridSize, image.shape[1])

            imagePixels[startEmptyRows:endFullRows, startEmptyColumns: endFullColumns] = \
                image[rowStartIndex:rowEndIndex, columnStartIndex:columnEndIndex]

        return imagePixels