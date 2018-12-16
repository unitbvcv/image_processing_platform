import numpy

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot

import Application.Settings
from Application import PlottingAlgorithms
from Application.Models.MainModel import MainModel
from Application.ViewModels.MainWindowVM import MainWindowVM
from Application.ViewModels.MagnifierWindowVM import MagnifierWindowVM
from Application.ViewModels.PlotterWindowVM import PlotterWindowVM


class MainVM(QtCore.QObject):
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
        self._model = MainModel()

        # Instantiate MainWindowViewModel
        self._mainWindowVM = MainWindowVM(self)
        self._mainWindowVM.loadOriginalImageSignal.connect(self.onLoadImageAction)

        # Instantiate MagnifierViewModel
        self._magnifierVM = MagnifierWindowVM(self)

        # Instantiate PlotterViewModel
        self._plotterVM = PlotterWindowVM(self)
        self._plotterVM.needOriginalImageData.connect(self.onSendOriginalImagePlotterData)
        self._plotterVM.needProcessedImageData.connect(self.onSendProcessedImagePlotterData)

        # test
        self._magnifierVM.showWindow()
        self._plotterVM.showWindow()
        self.onLoadImageAction(r"C:\Users\vladv\OneDrive\Imagini\IMG_4308.JPG", False)

        self.imageClickedEvent(QtCore.QPoint(100, 100))

    # TODO: REMEMBER THAT APPLYING AN ALGORITHM ON THE PROCESSED IMAGE MUST SET PLOTTING DATA DIRTY + MAGNIFIER
    # TODO: REMEMBER TO CONVERT IMAGE TO BGR WHEN SAVING ON DISK

    @pyqtSlot(str, bool)
    def onLoadImageAction(self, filePath, asGreyscale):
        self._model.readOriginalImage(filePath, asGreyscale)  # should return bool if read was successful?
        self._model.processedImage = None
        self._model.clickPosition = None
        self.resetVMs()

        # setup main window
        self._mainWindowVM.showNewOriginalImage(self._model.originalImage)

        # setup magnifier
        if asGreyscale:
            self._magnifierVM.setMagnifierColorSpace(Application.Settings.MagnifierWindowSettings.ColorSpaces.GRAY)
        else:
            self._magnifierVM.setMagnifierColorSpace(Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB)

        # setup plotter
        for plottingFunction in PlottingAlgorithms.registeredAlgorithms.values():
            if plottingFunction.computeOnImageChanged:
                # self.onSendPlotterData(plottingFunction.name)
                # this is lazier :))
                self._plotterVM.setOriginalImageDataAsDirty(plottingFunction.name)
                self._plotterVM.setProcessedImageDataAsDirty(plottingFunction.name)

        if self._plotterVM.isVisible:
            self._plotterVM.refresh()

    @pyqtSlot(str)
    def onSendOriginalImagePlotterData(self, functionName):
        self._sendPlotterData(
            functionName,
            self._model.originalImage,
            self._plotterVM.updateOriginalImageFunctionData
        )

    @pyqtSlot(str)
    def onSendProcessedImagePlotterData(self, functionName):
        self._sendPlotterData(
            functionName,
            self._model.processedImage,
            self._plotterVM.updateProcessedImageFunctionData
        )

    def _sendPlotterData(self, functionName, image, updateFunction):
        plottingFunction = PlottingAlgorithms.registeredAlgorithms[functionName]
        args = plottingFunction.prepare(self._model)
        plottingDataList = plottingFunction(image, **args)
        plotDataItemsDict = {plottingData.name: plottingData.toPlotDataItem()
                         for plottingData in plottingDataList}
        updateFunction(plottingFunction.name, plotDataItemsDict)

    @pyqtSlot(QtCore.QPoint)
    def imageClickedEvent(self, clickPosition):
        """
        # TODO: document MainViewModel.imageClickedEvent
        :param clickPosition: QPoint
        :return:
        """

        self._model.clickPosition = clickPosition

        if self._magnifierVM.isVisible or self._magnifierVM.isVisible:
            # mainWindowVM.highlightPosition(clickPosition)
            # de desenat linia si coloana rosie de highlight
            pass

        magnifiedRegions = self._getMagnifiedRegions(clickPosition)
        self._magnifierVM.setMagnifiedPixels(*magnifiedRegions)

        for plottingFunction in PlottingAlgorithms.registeredAlgorithms.values():
            if plottingFunction.computeOnClick:
                self._plotterVM.setOriginalImageDataAsDirty(plottingFunction.name)
                self._plotterVM.setProcessedImageDataAsDirty(plottingFunction.name)

        if self._plotterVM.isVisible:
            self._plotterVM.refresh()

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

        imagePixels = numpy.full((frameGridSize, frameGridSize), None)

        if image is not None:
            if len(image.shape) == 3:
                imagePixels = numpy.full((frameGridSize, frameGridSize, image.shape[2]), None)

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

            imagePixels[startEmptyRows:endFullRows, startEmptyColumns:endFullColumns] = \
                image[rowStartIndex:rowEndIndex, columnStartIndex:columnEndIndex]

        return imagePixels

    def resetVMs(self):
        self._magnifierVM.reset()
        self._plotterVM.reset()
        self._mainWindowVM.reset()
