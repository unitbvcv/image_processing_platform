from PyQt5 import QtCore, QtWidgets
from Application.Models import Model
from Application.ViewModels import MagnifierWindowViewModel
import Application.Settings
import numpy as np


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

    def imageClickedEvent(self, clickPosition):
        """
        # TODO: document MainViewModel.imageClickedEvent
        :param clickPosition: QPoint
        :return:
        """
        if self._magnifierVM.isVisible: # sau plotterul
            # mainWindow.highlightPosition(clickPosition)

            magnifiedRegions = self._getMagnifiedRegions(clickPosition)
            self._magnifierVM.setMagnifiedPixels(*magnifiedRegions)

            # set plotter parameters

    def _getMagnifiedRegions(self, clickPosition):
        """
        # TODO: document MainViewModel._getMagnifiedRegions
        :param clickPosition: QPoint
        :return:
        """
        frameGridSize = Application.Settings.MagnifierWindowSettings.frameGridSize
        offset = frameGridSize // 2

        yPos = clickPosition.y()
        xPos = clickPosition.x()

        rowStartIndex = yPos - offset if yPos - offset >= 0 else 0
        columnStartIndex = xPos - offset if xPos - offset >= 0 else 0

        originalImagePixels = np.full((frameGridSize, frameGridSize), None)

        if self._model.originalImage is not None:
            rowEndIndex = yPos + offset + 1 if yPos + offset + 1 <= self._model.originalImage.shape[0] else self._model.originalImage.shape[0]
            columnEndIndex = xPos + offset + 1 if xPos + offset + 1 <= self._model.originalImage.shape[1] else self._model.originalImage.shape[1]

            originalImagePixels[rowStartIndex:rowEndIndex, columnStartIndex:columnEndIndex] = \
                self._model.originalImage[rowStartIndex:rowEndIndex, columnStartIndex:columnEndIndex]

        processedImagePixels = np.full((frameGridSize, frameGridSize), None)

        if self._model.processedImage is not None:
            rowEndIndex = yPos + offset + 1 if yPos + offset + 1 <= self._model.processedImage.shape[0] else self._model.processedImage.shape[0]
            columnEndIndex = xPos + offset + 1 if xPos + offset + 1 <= self._model.processedImage.shape[1] else self._model.processedImage.shape[1]

            processedImagePixels[rowStartIndex:rowEndIndex, columnStartIndex:columnEndIndex] = \
                self._model.processedImage[rowStartIndex:rowEndIndex, columnStartIndex:columnEndIndex]

        return originalImagePixels, processedImagePixels
