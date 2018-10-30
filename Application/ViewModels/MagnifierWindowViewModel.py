from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot
from Application.Models import MagnifierWindowModel
from Application.Views import MagnifierWindow
import Application.Settings

class MagnifierWindowViewModel(QtCore.QObject):
    """
    TODO: document MagnifierWindowViewModel
    """

    windowClosing = QtCore.pyqtSignal(QtGui.QCloseEvent, name="windowClosing")

    def __init__(self, parent=None):
        """
        TODO: document MagnifierWindowViewModel constructor
        :param parent:
        """
        super().__init__(parent)

        # Instantiate the model
        self._model = MagnifierWindowModel()

        # Instantiate the view
        self._view = MagnifierWindow()

        # Connect the view
        self._view.comboBoxColorSpace.currentIndexChanged[int].connect(self._magnifierColorSpaceIndexChanged)
        self._view.closing.connect(self.windowClosing)

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
        return self._view.isVisible()

    def setMagnifierColorSpace(self, colorSpace : Application.Settings.MagnifierWindowSettings.ColorSpaces):
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
        Application.Settings.MagnifierWindowSettings.fontSize = 2
        self._model.colorSpace = Application.Settings.MagnifierWindowSettings.aa
        self._view.setColorSpace(self._model.colorSpace)

    def setMagnifiedPixels(self, originalImagePixels, processedImagePixels):
        """
        TODO: document MagnifierWindowViewModel.setMagnifiedPixels
        :param originalImagePixels:
        :param processedImagePixels:
        :return:
        """
        frameGridSize = Application.Settings.MagnifierWindowSettings.frameGridSize

        for row in range(frameGridSize):
            for column in range(frameGridSize):
                pixelOriginalImageColor = originalImagePixels[row, column]
                self._view.setOriginalPixelFrameColor(row, column, pixelOriginalImageColor)

                pixelProcessedImageColor = processedImagePixels[row, column]
                self._view.setProcessedPixelFrameColor(row, column, pixelProcessedImageColor)

    def resetMagnifier(self):
        """Clears the magnifier window.

        Resetting the model isn't necessary as the view will reset it indirectly through the VM.

        Returns:
            None

        """
        self._view.reset()
