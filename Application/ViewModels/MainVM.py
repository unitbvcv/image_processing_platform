import numpy

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import pyqtSlot

import Application.Settings
from Application import PlottingAlgorithms
from Application import ImageProcessingAlgorithms
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
        self._plotterVM.registerFunctions(list(Application.PlottingAlgorithms.registeredAlgorithms.keys()))
        self._plotterVM.needOriginalImageData.connect(self.onSendOriginalImagePlotterData)
        self._plotterVM.needProcessedImageData.connect(self.onSendProcessedImagePlotterData)

        self._mainWindowVM.openPlotterSignal.connect(self._onOpenPlotterAction)
        self._mainWindowVM.openMagnifierSignal.connect(self._onOpenMagnifierAction)

        self._mainWindowVM.saveAsOriginalImageSignal.connect(self._onSaveAsOriginalImageAction)
        self._mainWindowVM.saveProcessedImageSignal.connect(self._onSaveProcessedImageAction)

        self._mainWindowVM.mouseMovedImageLabelSignal.connect(self._onMouseMovedImageLabel)
        self._mainWindowVM.mousePressedImageLabelSignal.connect(self._onMousePressedImageLabel)

        self._magnifierVM.windowClosingSignal.connect(self._onMagnifierOrPlotterWindowClose)
        self._plotterVM.windowClosingSignal.connect(self._onMagnifierOrPlotterWindowClose)

        self._mainWindowVM.keyPressedSignal.connect(self._onKeyPressed)

    # TODO: REMEMBER THAT APPLYING AN ALGORITHM ON THE PROCESSED IMAGE MUST SET PLOTTING DATA DIRTY + MAGNIFIER
    # TODO: all the algorithms' qactions can connect to the same slot which checks if origImage is not None

    @pyqtSlot(QtGui.QCloseEvent)
    def _onMagnifierOrPlotterWindowClose(self, QCloseEvent):
        if not self._magnifierVM.isVisible and not self._plotterVM.isVisible:
            self._mainWindowVM.highlightImageLabelLeftClickPosition(None)
            self._model.leftClickPosition = None
            self._magnifierVM.clear()

            for plottingFunction in PlottingAlgorithms.registeredAlgorithms.values():
                if plottingFunction.computeOnClick:
                    self._plotterVM.setOriginalImageDataAsDirty(plottingFunction.name)
                    self._plotterVM.setProcessedImageDataAsDirty(plottingFunction.name)

    @pyqtSlot(QtCore.QPoint)
    def _onMouseMovedImageLabel(self, clickPosition):
        x = clickPosition.x()
        y = clickPosition.y()

        labelText = ''

        if self._model.originalImage is not None or self._model.processedImage is not None:
            labelText = f'Mouse position: (X, Y) = ({x}, {y})'
        self._mainWindowVM.setMousePositionLabelText(labelText)

        labelText = ''

        # updating original image pixel label
        if self._model.originalImage is not None:
            if len(self._model.originalImage.shape) == 3:
                pixel = self._model.originalImage[y][x]
                labelText = f'(R, G, B) = ({pixel[0]}, {pixel[1]}, {pixel[2]})'
            elif len(self._model.originalImage.shape) == 2:
                pixel = self._model.originalImage[y][x]
                labelText = f'(Gray) = ({pixel})'
        self._mainWindowVM.setOriginalImagePixelValueLabelText(labelText)

        labelText = ''

        # updating processed image pixel label
        if self._model.processedImage is not None:
            if len(self._model.processedImage.shape) == 3:
                pixel = self._model.processedImage[y][x]
                labelText = f'(R, G, B) = ({pixel[0]}, {pixel[1]}, {pixel[2]})'
            elif len(self._model.processedImage.shape) == 2:
                pixel = self._model.processedImage[y][x]
                labelText = f'(Gray) = ({pixel})'
        self._mainWindowVM.setProcessedImagePixelValueLabelText(labelText)

    @pyqtSlot(str)
    def _onSaveProcessedImageAction(self, filePath):
        self._model.saveProcessedImage(filePath)

    @pyqtSlot()
    def _onSaveAsOriginalImageAction(self):
        self._model.originalImage = self._model.processedImage
        self._model.processedImage = None
        self.resetVMs()

        # setup main window
        self._mainWindowVM.showNewOriginalImage(self._model.originalImage)

        # tell the magnifier we still have a click
        if self._model.leftClickPosition is not None:
            self._onMousePressedImageLabel(self._model.leftClickPosition, QtCore.Qt.LeftButton)

        if self._model.rightClickLastPositions.__len__() > 0:
            for (x, y) in self._model.rightClickLastPositions:
                self._onMousePressedImageLabel(QtCore.QPoint(x, y), QtCore.Qt.RightButton)

        if self._plotterVM.isVisible:
            self._plotterVM.refresh()

    @pyqtSlot()
    def _onOpenPlotterAction(self):
        self._plotterVM.showWindow()

    @pyqtSlot()
    def _onOpenMagnifierAction(self):
        self._magnifierVM.showWindow()

    @pyqtSlot(str, bool)
    def onLoadImageAction(self, filePath, asGreyscale):
        self._model.readOriginalImage(filePath, asGreyscale)  # should return bool if read was successful?
        self._model.processedImage = None
        self._model.leftClickPosition = None
        self._model.rightClickLastPositions.clear()
        self.resetVMs()

        # setup main window
        self._mainWindowVM.showNewOriginalImage(self._model.originalImage)

        # setup magnifier
        if asGreyscale:
            self._magnifierVM.setMagnifierColorSpace(Application.Settings.MagnifierWindowSettings.ColorSpaces.GRAY)
        else:
            self._magnifierVM.setMagnifierColorSpace(Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB)

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
        if image is not None:
            plottingFunction = PlottingAlgorithms.registeredAlgorithms[functionName]
            args = plottingFunction.prepare(self._model)
            plottingDataList = plottingFunction(image, **args)
            plotDataItemsDict = {plottingData.name: plottingData.toPlotDataItem()
                             for plottingData in plottingDataList}
            updateFunction(plottingFunction.name, plotDataItemsDict)

    @pyqtSlot(QtGui.QKeyEvent)
    def _onKeyPressed(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Escape:
            self._model.rightClickLastPositions.clear()
            self._mainWindowVM.highlightImageLabelRightClickLastPositions(None)

    @pyqtSlot(QtCore.QPoint, QtCore.Qt.MouseButton)
    def _onMousePressedImageLabel(self, clickPosition, mouseButton):
        """
        # TODO: document MainViewModel.imageClickedEvent
        :param clickPosition: QPoint
        :return:
        """
        if mouseButton == QtCore.Qt.LeftButton:
            if self._magnifierVM.isVisible or self._plotterVM.isVisible:
                self._model.leftClickPosition = clickPosition

                self._mainWindowVM.highlightImageLabelLeftClickPosition(clickPosition)

                magnifiedRegions = self._getMagnifiedRegions(clickPosition)
                self._magnifierVM.setMagnifiedPixels(*magnifiedRegions)

                for plottingFunction in PlottingAlgorithms.registeredAlgorithms.values():
                    if plottingFunction.computeOnClick:
                        self._plotterVM.setOriginalImageDataAsDirty(plottingFunction.name)
                        self._plotterVM.setProcessedImageDataAsDirty(plottingFunction.name)

                if self._plotterVM.isVisible:
                    self._plotterVM.refresh()

        elif mouseButton == QtCore.Qt.RightButton:
            self._addRightClickPosition(clickPosition)

    def _addRightClickPosition(self, clickPosition):
        self._model.rightClickLastPositions.appendleft((clickPosition.x(), clickPosition.y()))
        self._mainWindowVM.highlightImageLabelRightClickLastPositions(self._model.rightClickLastPositions)

    def _clearRightClickLastPositions(self):
        self._model.rightClickLastPositions.clear()
        self._mainWindowVM.highlightImageLabelRightClickLastPositions(None)

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

            startIndexes = lambda pos, offset: (pos - offset, 0) if pos - offset >= 0 else (0, offset - pos)
            rowStartIndex, startEmptyRows = startIndexes(clickPosition.y(), frameOffset)
            columnStartIndex, startEmptyColumns = startIndexes(clickPosition.x(), frameOffset)

            endIndexes = lambda pos, offset, gridSize, imageSize: \
                (pos + offset + 1, gridSize) if pos + offset + 1 <= imageSize else (imageSize, offset + imageSize - pos)
            rowEndIndex, endFullRows = endIndexes(clickPosition.y(), frameOffset, frameGridSize, image.shape[0])
            columnEndIndex, endFullColumns = endIndexes(clickPosition.x(), frameOffset, frameGridSize, image.shape[1])

            imagePixels[startEmptyRows:endFullRows, startEmptyColumns:endFullColumns] = \
                image[rowStartIndex:rowEndIndex, columnStartIndex:columnEndIndex]

        return imagePixels

    def resetVMs(self):
        self._magnifierVM.clear()
        self._plotterVM.reset()
        self._mainWindowVM.reset()
