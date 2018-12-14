from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot

from Application.Models.PlotterWindowModel import PlotterWindowModel
from Application.Models.PlottingFunctionModel import PlottingFunctionModel
from Application.Views.PlotterWindowView import PlotterWindowView
import Application.PlottingAlgorithms as PlottingAlgorithms


class PlotterWindowVM(QtCore.QObject):
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
        for functionName in PlottingAlgorithms.registeredAlgorithms.keys():
            self._model.functionModels[functionName] = PlottingFunctionModel()

        # Instantiate the view
        self._view = PlotterWindowView()

        # Connect the view
        self._view.closing.connect(self.closingWindow)
        self._view.comboBoxFunction.currentIndexChanged[int].connect(self._functionComboBoxIndexChanged)
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

    def setDirtyData(self, functionName : str):
        self._model.functionModels[functionName].isDirty = True

    def refresh(self):
        pass

    def reset(self):
        """
        TODO: document PlotterWindowViewModel resetPlotter
        :return:
        """
        # Clearing the view
        self._view.clearPlotItems()
        #TODO: verifica daca mai e necesar clear pe legend
        self._view.clearPlotItemsLegends(self._model.visiblePlotDataItemsOriginalImage.keys(),
                                         self._model.visiblePlotDataItemsProcessedImage.keys())
        self._view.clearListWidgets()

        # Clearing the model
        self._model.visiblePlotDataItemsOriginalImage.clear()
        self._model.visiblePlotDataItemsProcessedImage.clear()

        self._model.availablePlotDataItemsOriginalImage.clear()
        self._model.availablePlotDataItemsProcessedImage.clear()

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

    def _visiblePlotsSelectionChanged(self, plotItem, availablePlotDataItems, visiblePlotDataItems, listWidget):
        """
        TODO: document PlotterWindowViewModel _visiblePlotsSelectionChanged
        :param plotItem:
        :param availablePlotDataItems:
        :param visiblePlotDataItems:
        :param listWidget:
        :return:
        """
        selectedPlotsNames = set([item.text() for item in listWidget.selectedItems()])
        visiblePlotsNames = set(visiblePlotDataItems.keys())

        if selectedPlotsNames > visiblePlotsNames:
            # here one or more plots have been selected
            plotDataItemsNamesToAdd = selectedPlotsNames - visiblePlotsNames

            plotDataItemsToAdd = []

            # adding the plots in model from available to visible
            for plotDataItemName in plotDataItemsNamesToAdd:
                plotDataItem = availablePlotDataItems[plotDataItemName]
                visiblePlotDataItems[plotDataItemName] = plotDataItem
                plotDataItemsToAdd.append(plotDataItem)

            # updating the view
            self._view.addPlotDataItems(plotItem, plotDataItemsToAdd)

        elif visiblePlotsNames > selectedPlotsNames:
            # here one or more plots have been deselected
            plotDataItemsNamesToRemove = visiblePlotsNames - selectedPlotsNames

            plotDataItemsToRemove = [plotDataItem for (plotDataItemName, plotDataItem)
                                     in visiblePlotDataItems.items()
                                     if plotDataItemName in plotDataItemsNamesToRemove]

            # removing them from view
            self._view.removePlotDataItems(plotItem, plotDataItemsToRemove)

            # removing them from the visible plots in the model
            for plotDataItemName in plotDataItemsNamesToRemove:
                del visiblePlotDataItems[plotDataItemName]

    @pyqtSlot()
    def _visiblePlotsOriginalImageSelectionChangedEvent(self):
        """
        TODO document PlotterWindowViewModel _visiblePlotsOriginalImageSelectionChangedEvent
        :return:
        """
        self._visiblePlotsSelectionChanged(
            self._view.plotItemOriginalImage,
            self._model.availablePlotDataItemsOriginalImage,
            self._model.visiblePlotDataItemsOriginalImage,
            self._view.listWidgetVisibleOriginalImage)

    @pyqtSlot()
    def _visiblePlotsProcessedImageSelectionChangedEvent(self):
        """
        TODO: document PlotterWindowViewModel _visiblePlotsProcessedImageSelectionChangedEvent
        :return:
        """
        self._visiblePlotsSelectionChanged(
            self._view.plotItemProcessedImage,
            self._model.availablePlotDataItemsProcessedImage,
            self._model.visiblePlotDataItemsProcessedImage,
            self._view.listWidgetVisibleProcessedImage)


# pentru plotare e nevoie de poze; sugestie:
# cand se schimba functia din combo box, ploterul emite un semnal si mainVM apeleaza refreshPlotter
# si ii da ca parametrii cele 2 poze si last clickul (asemanator cu calculateAndSetParam..)
#
# la ckick event se apeleaza tot refreshPlotter
#
