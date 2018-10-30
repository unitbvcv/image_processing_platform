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
        self._view.pushButtonScaleAndCenter.pressed.connect(self._scaleAndCenterButtonPressed)

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

    @pyqtSlot()
    def _scaleAndCenterButtonPressed(self):
        """
        TODO: document PlotterWindowViewModel _scaleAndCenterButtonPressed
        :return:
        """
        plots = list(self._model.visiblePlotDataItemsOriginalImage.values()) + \
            list(self._model.visiblePlotDataItemsProcessedImage.values())

        self._view.scaleAndCenterToPlots(plots)

    @pyqtSlot(int)
    def _functionComboBoxIndexChanged(self, index):
        pass

    @pyqtSlot()
    def _visiblePlotsOriginalImageSelectionChangedEvent(self):
        selectedPlotsNames = set([item.text() for item in self._view.listWidgetVisibleOriginalImage.selectedItems()])
        visiblePlotsNames = set(self._model.visiblePlotDataItemsOriginalImage.keys())

        if selectedPlotsNames > visiblePlotsNames:
            # aici s-au activat plot-uri
            plotsToAdd = selectedPlotsNames - visiblePlotsNames

        elif visiblePlotsNames > selectedPlotsNames:
            # here one or more plots have been deselected
            plotsToRemove = visiblePlotsNames - selectedPlotsNames

            # removing them from the visible plots in the model
            for plotName in plotsToRemove:
                del self._model.visiblePlotDataItemsOriginalImage[plotName]

            # removing them from view
            self._view.removePlotDataItemsFromOriginalImage(self._model.visiblePlotDataItemsOriginalImage.values())



    @pyqtSlot()
    def _visiblePlotsProcessedImageSelectionChangedEvent(self):
        pass

    def resetPlotter(self):
        """
        TODO: document PlotterWindowViewModel resetPlotter
        :return:
        """
        # Clearing the view
        self._view.clearPlotItems()
        self._view.clearPlotItemsLegends(self._model.visiblePlotDataItemsOriginalImage.keys(),
                                         self._model.visiblePlotDataItemsProcessedImage.keys())
        self._view.clearListWidgets()

        # Clearing the model
        self._model.visiblePlotDataItemsOriginalImage.clear()
        self._model.visiblePlotDataItemsProcessedImage.clear()

        self._model.availablePlotDataItemsOriginalImage.clear()
        self._model.availablePlotDataItemsProcessedImage.clear()


# de facut selectia pe list widget cu diferenta de seturi - se poate face intern
#
# pentru plotare e nevoie de poze; sugestie:
# cand se schimba functia din combo box, ploterul emite un semnal si mainVM apeleaza refreshPlotter
# si ii da ca parametrii cele 2 poze si last clickul (asemanator cu calculateAndSetParam..)
#
# la ckick event se apeleaza tot refreshPlotter
#
