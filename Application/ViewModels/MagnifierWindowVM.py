from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot, pyqtSignal

from Application.Settings import MagnifierWindowSettings
from Application.Models.MagnifierWindowModel import MagnifierWindowModel
from Application.Views.MagnifierWindowView import MagnifierWindowView


class MagnifierWindowVM(QtCore.QObject):
    """
    TODO: document MagnifierWindowViewModel
    """

    windowClosingSignal = pyqtSignal(QtGui.QCloseEvent, name="windowClosingSignal")

    def __init__(self, parent=None):
        """
        TODO: document MagnifierWindowViewModel constructor
        :param parent:
        """
        super().__init__(parent)

        # Instantiate the model
        self._model = MagnifierWindowModel()

        # Instantiate the view
        self._view = MagnifierWindowView()

        # Connect the view
        self._view.comboBoxColorSpace.currentIndexChanged[int].connect(self._magnifierColorSpaceIndexChanged)
        self._view.windowClosingSignal.connect(self.windowClosingSignal)

    def showWindow(self):
        """Shows the magnifier window.

        Returns:
             None

        """
        self._view.show()

    @property
    def isVisible(self):
        """
        TODO: document MagnifierWindowViewModel.isVisible
        :return:
        """
        return self._view.isWindowVisible

    def setMagnifierColorSpace(self, colorSpace : MagnifierWindowSettings.ColorSpaces):
        """
        TODO: document MagnifierWindowViewModel.setMagnifierColorSpace
        :param colorSpace:
        :return:
        """
        self._model.colorSpace = colorSpace
        self._view.comboBoxColorSpace.setCurrentIndex(colorSpace.value[0])

    @pyqtSlot(int)
    def _magnifierColorSpaceIndexChanged(self, index):
        """
        TODO: document MagnifierWindowViewModel._magnifierColorSpaceIndexChanged
        :param index:
        :return:
        """

        self._model.colorSpace = MagnifierWindowSettings.colorSpacesDict[index]
        self._view.setColorSpace(self._model.colorSpace)

    def setMagnifiedPixels(self, originalImagePixels, processedImagePixels):
        """
        TODO: document MagnifierWindowViewModel.setMagnifiedPixels
        :param originalImagePixels:
        :param processedImagePixels:
        :return:
        """
        frameGridSize = MagnifierWindowSettings.frameGridSize

        for row in range(frameGridSize):
            for column in range(frameGridSize):
                pixelOriginalImageColor = originalImagePixels[row, column]
                self._view.setOriginalPixelFrameColor(row, column, pixelOriginalImageColor)

                pixelProcessedImageColor = processedImagePixels[row, column]
                self._view.setProcessedPixelFrameColor(row, column, pixelProcessedImageColor)

    def reset(self):
        """Clears the magnifier window.

        Resetting the model isn't necessary as the view will reset it indirectly through the VM.

        Returns:
            None

        """
        self._view.reset()
