from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from Application.Models import PlotterWindowModel
from Application.Views import PlotterWindow


class PlotterWindowViewModel(QtWidgets.QWidget):
    """
    TODO: document PlotterWindowViewModel
    """

    closingWindow = QtCore.pyqtSignal(QtGui.QCloseEvent, name="closingWindow")

    def __init__(self, parent=None):
        """
        TODO: document PlotterWindowViewModel constructor
        :param parent:
        """
        super().__init__(parent)

        # Instantiate the model
        self._model = PlotterWindowModel()

        # Instantiate the view
        self._view = PlotterWindow(self)

        # Connect the view
        self._view.closing.connect(self.closingWindow)
        self._view.comboBoxFunction.currentIndexChanged[int](self._functionComboBoxIndexChanged())
        self._view.listWidgetVisibleOriginalImage.itemSelectionChanged.connect(
            self._visiblePlotsOriginalImageSelectionChangedEvent)
        self._view.listWidgetVisibleProcessedImage.itemSelectionChanged.connect(
            self._visiblePlotsProcessedImageSelectionChangedEvent)

    def showWindow(self):
        """Shows the plotter window.

        Returns:
             None

        """
        self._view.show()

    @property
    def isVisible(self):
        """
        TODO: document PlotterWindowViewModel.isVisible
        :return:
        """
        return self._view.isVisible()

    @pyqtSlot(int)
    def _functionComboBoxIndexChanged(self, index):
        pass

    @pyqtSlot()
    def _visiblePlotsOriginalImageSelectionChangedEvent(self):
        pass

    @pyqtSlot()
    def _visiblePlotsProcessedImageSelectionChangedEvent(self):
        pass
