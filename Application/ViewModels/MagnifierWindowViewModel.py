from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from Application.Models import MagnifierWindowModel
from Application.Views import MagnifierWindow
import Application.Settings

class MagnifierWindowViewModel(QtWidgets.QWidget):
    """
    TODO: document MagnifierWindowViewModel
    """

    def __init__(self, parent=None):
        """
        TODO: document MagnifierWindowViewModel constructor
        :param parent:
        """

        # aici sau in mainVM? sau in Settings? se pot pune in implementarea proprietatilor, dar e ineficient
        assert (Application.Settings.MagnifierWindowSettings.frameGridSize % 2 == 1)
        assert (Application.Settings.MagnifierWindowSettings.frameGridSize > 0)
        assert (Application.Settings.MagnifierWindowSettings.fontSize > 0)

        super().__init__(parent)

        # Instantiate the model
        self._model = MagnifierWindowModel()

        # Instantiate the view
        self._view = MagnifierWindow(self)

        # Connect the view
        self._view.comboBoxColorSpace.currentIndexChanged[int].connect(self._magnifierColorSpaceIndexChanged)

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
        self._view.setColorSpace(self._model.colorSpace)

    def setMagnifiedPixels(self, originalImagePixels, processedImagePixels):
        pass

    # TODO: a reset function
