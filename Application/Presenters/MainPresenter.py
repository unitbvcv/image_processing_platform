import numpy
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Slot
import traceback
import sys

import Application.Settings
from Application import PlottingAlgorithms
from Application import ImageProcessingAlgorithms
from Application.Models.MainModel import MainModel
from Application.Presenters.MainWindowPresenter import MainWindowPresenter
from Application.Presenters.MagnifierWindowPresenter import MagnifierWindowPresenter
from Application.Presenters.PlotterWindowPresenter import PlotterWindowPresenter
from Application.Utils.Point import Point


class MainPresenter(QtCore.QObject):
    """
    TODO: document MainPresenter class
    """

    def __init__(self, parent=None):
        """
        # TODO: document MainPresenter constructor
        :param parent:
        """
        super().__init__(parent)

        # Instantiate MainModel
        self._model = MainModel()

        # Instantiate MainWindowPresenter
        self._mainWindowPresenter = MainWindowPresenter(self)
        self._mainWindowPresenter.loadOriginalImageSignal.connect(self.onLoadImageAction)

        # Create UI for the registered algorithms and connect them
        self._populateMenuBarWithAlgorithms()
        self._mainWindowPresenter.algorithmTriggered.connect(self._onAlgorithmTriggerred)

        # Instantiate MagnifierPresenter
        self._magnifierPresenter = MagnifierWindowPresenter(self)

        # Instantiate PlotterPresenter
        self._plotterPresenter = PlotterWindowPresenter(self)
        self._plotterPresenter.registerFunctions(list(Application.PlottingAlgorithms.registeredAlgorithms.keys()))
        self._plotterPresenter.needOriginalImageData.connect(self.onSendOriginalImagePlotterData)
        self._plotterPresenter.needProcessedImageData.connect(self.onSendProcessedImagePlotterData)

        self._mainWindowPresenter.openPlotterSignal.connect(self._onOpenPlotterAction)
        self._mainWindowPresenter.openMagnifierSignal.connect(self._onOpenMagnifierAction)

        self._mainWindowPresenter.saveAsOriginalImageSignal.connect(self._onSaveAsOriginalImageAction)
        self._mainWindowPresenter.saveProcessedImageSignal.connect(self._onSaveProcessedImageAction)

        self._mainWindowPresenter.mouseMovedImageLabelSignal.connect(self._onMouseMovedImageLabel)
        self._mainWindowPresenter.mousePressedImageLabelSignal.connect(self._onMousePressedImageLabel)

        self._magnifierPresenter.windowClosingSignal.connect(self._onMagnifierOrPlotterWindowClose)
        self._plotterPresenter.windowClosingSignal.connect(self._onMagnifierOrPlotterWindowClose)

        self._mainWindowPresenter.keyPressedSignal.connect(self._onKeyPressed)

    def _populateMenuBarWithAlgorithms(self):
        algorithms = [(algorithm.name, algorithm.menuPath, algorithm.before)
                      for algorithm in ImageProcessingAlgorithms.registeredAlgorithms.values()]
        self._mainWindowPresenter.registerAlgorithmsInUi(algorithms)

    @Slot(str)
    def _onAlgorithmTriggerred(self, algorithmName):
        if self._model.originalImage is not None:
            algorithm = ImageProcessingAlgorithms.registeredAlgorithms[algorithmName]
            args = algorithm.prepare(self._model)
            try:
                algorithm(self._model.originalImage.copy(), **args)

                if algorithm.hasResult:
                    # Check for original image
                    newOriginalImage = algorithm.result.get('originalImage')
                    if newOriginalImage is not None:
                        self._model.originalImage = newOriginalImage
                        self._mainWindowPresenter.setOriginalImage(self._model.originalImage)

                    # Check for processed image
                    newProcessedImage = algorithm.result.get('processedImage')
                    if newProcessedImage is not None:
                        self._model.processedImage = newProcessedImage
                        self._mainWindowPresenter.setProcessedImage(self._model.processedImage)

                    # Check for original image overlay drawing
                    overlayData = algorithm.result.get('originalImageOverlayData')
                    self._mainWindowPresenter.setOriginalImageOverlayData(overlayData)

                    # Check for processed image overlay drawing
                    overlayData = algorithm.result.get('processedImageOverlayData')
                    self._mainWindowPresenter.setProcessedImageOverlayData(overlayData)

                    if self._model.leftClickPosition is not None:
                        self._onMousePressedImageLabel(self._model.leftClickPosition, QtCore.Qt.LeftButton)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                messagebox = QtWidgets.QMessageBox(self._mainWindowPresenter._view)
                messagebox.setWindowTitle("Image processing algorithm error")
                messagebox.setText('\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
                messagebox.setIcon(QtWidgets.QMessageBox.Critical)
                messagebox.exec()
        else:
            messagebox = QtWidgets.QMessageBox(self._mainWindowPresenter._view)
            messagebox.setWindowTitle("Image processing algorithm warning")
            messagebox.setText("Algorithm not executed: no source image")
            messagebox.setIcon(QtWidgets.QMessageBox.Warning)
            messagebox.exec()
                
    @Slot(QtGui.QCloseEvent)
    def _onMagnifierOrPlotterWindowClose(self, QCloseEvent):
        if not self._magnifierPresenter.isVisible and not self._plotterPresenter.isVisible:
            self._mainWindowPresenter.highlightImageLabelLeftClickPosition(None)
            self._model.leftClickPosition = None
            self._magnifierPresenter.clear()

            for plottingFunction in PlottingAlgorithms.registeredAlgorithms.values():
                if plottingFunction.computeOnClick:
                    self._plotterPresenter.setOriginalImageDataAsDirty(plottingFunction.name)
                    self._plotterPresenter.setProcessedImageDataAsDirty(plottingFunction.name)

    @Slot(Point)
    def _onMouseMovedImageLabel(self, clickPosition):
        x, y = clickPosition

        labelText = ''

        if self._model.originalImage is not None or self._model.processedImage is not None:
            labelText = f'Mouse position: (X, Y) = ({x}, {y})'
        self._mainWindowPresenter.setMousePositionLabelText(labelText)

        labelText = ''

        # updating original image pixel label
        if self._model.originalImage is not None:
            if y < self._model.originalImage.shape[0] and x < self._model.originalImage.shape[1] and y >= 0 and x >= 0:
                originalImageShapeLen = len(self._model.originalImage.shape)
                if originalImageShapeLen == 3:
                    pixel = self._model.originalImage[y][x]
                    labelText = f'(R, G, B) = ({pixel[0]}, {pixel[1]}, {pixel[2]})'
                elif originalImageShapeLen == 2:
                    pixel = self._model.originalImage[y][x]
                    labelText = f'(Gray) = ({pixel})'
            self._mainWindowPresenter.setOriginalImagePixelValueLabelText(labelText)

        labelText = ''

        # updating processed image pixel label
        if self._model.processedImage is not None:
            if y < self._model.processedImage.shape[0] and x < self._model.processedImage.shape[1] and y >= 0 and x >= 0:
                processedImageShapeLen = len(self._model.processedImage.shape)
                if processedImageShapeLen == 3:
                    pixel = self._model.processedImage[y][x]
                    labelText = f'(R, G, B) = ({pixel[0]}, {pixel[1]}, {pixel[2]})'
                elif processedImageShapeLen == 2:
                    pixel = self._model.processedImage[y][x]
                    labelText = f'(Gray) = ({pixel})'
            self._mainWindowPresenter.setProcessedImagePixelValueLabelText(labelText)

    @Slot(str)
    def _onSaveProcessedImageAction(self, filePath):
        self._model.saveProcessedImage(filePath)

    @Slot()
    def _onSaveAsOriginalImageAction(self):
        processedImageCopy = self._model.processedImage
        self._model.reset()
        self._model.originalImage = processedImageCopy
        self.resetPresenters()

        # setup main window
        self._mainWindowPresenter.setOriginalImage(self._model.originalImage)
        self._mainWindowPresenter.setProcessedImage(None)

        # tell the magnifier we still have a click
        if self._model.leftClickPosition is not None:
            self._onMousePressedImageLabel(self._model.leftClickPosition, QtCore.Qt.LeftButton)

        for point in self._model.rightClickLastPositions:
            self._onMousePressedImageLabel(point, QtCore.Qt.RightButton)

        if self._plotterPresenter.isVisible:
            self._plotterPresenter.refresh()

    @Slot()
    def _onOpenPlotterAction(self):
        self._plotterPresenter.showWindow()

    @Slot()
    def _onOpenMagnifierAction(self):
        self._magnifierPresenter.showWindow()

    @Slot(str, bool)
    def onLoadImageAction(self, filePath, asGreyscale):
        self._model.reset()
        self._model.readOriginalImage(filePath, asGreyscale)  # should return bool if read was successful?
        self.resetPresenters()

        # setup main window
        self._mainWindowPresenter.setOriginalImage(self._model.originalImage)
        self._mainWindowPresenter.setProcessedImage(None)

        # setup magnifier
        if asGreyscale:
            self._magnifierPresenter.setMagnifierColorSpace(Application.Settings.MagnifierWindowSettings.ColorSpaces.GRAY)
        else:
            self._magnifierPresenter.setMagnifierColorSpace(Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB)

        if self._plotterPresenter.isVisible:
            self._plotterPresenter.refresh()

    @Slot(str)
    def onSendOriginalImagePlotterData(self, functionName):
        self._sendPlotterData(
            functionName,
            self._model.originalImage,
            self._plotterPresenter.updateOriginalImageFunctionData
        )

    @Slot(str)
    def onSendProcessedImagePlotterData(self, functionName):
        self._sendPlotterData(
            functionName,
            self._model.processedImage,
            self._plotterPresenter.updateProcessedImageFunctionData
        )

    def _sendPlotterData(self, functionName, image, updateFunction):
        if image is not None:  # probably move this down 2 lines
            plottingFunction = PlottingAlgorithms.registeredAlgorithms[functionName]
            args = plottingFunction.prepare(self._model)
            try:
                plottingFunction(image, **args)
                if plottingFunction.hasResult:
                    if plottingFunction.result is None:
                        plottingFunction.setResult({})
                    plottingDataList = plottingFunction.result.get('plottingDataList')
                    if plottingDataList is None:
                        plottingDataList = []
                    plotDataItemsDict = {plottingData.name: plottingData.toPlotDataItem()
                                        for plottingData in plottingDataList}
                    updateFunction(plottingFunction.name, plotDataItemsDict)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                messagebox = QtWidgets.QMessageBox(self._plotterPresenter._view)
                messagebox.setWindowTitle("Plotting algorithm error")
                messagebox.setText('\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
                messagebox.setIcon(QtWidgets.QMessageBox.Critical)
                messagebox.exec()

    @Slot(QtGui.QKeyEvent)
    def _onKeyPressed(self, QKeyEvent):
        if QKeyEvent.key() == QtCore.Qt.Key_Escape:
            self._model.rightClickLastPositions.clear()
            self._mainWindowPresenter.highlightImageLabelRightClickLastPositions(None)

    @Slot(Point, QtCore.Qt.MouseButton)
    def _onMousePressedImageLabel(self, clickPosition, mouseButton):
        """
        # TODO: document MainPresenter.imageClickedEvent
        :param clickPosition: Utils.Point
        :return:
        """
        if mouseButton == QtCore.Qt.LeftButton:
            if self._magnifierPresenter.isVisible or self._plotterPresenter.isVisible:
                self._model.leftClickPosition = clickPosition

                self._mainWindowPresenter.highlightImageLabelLeftClickPosition(clickPosition)

                magnifiedRegions = self._getMagnifiedRegions(clickPosition)
                self._magnifierPresenter.setMagnifiedPixels(*magnifiedRegions)

                for plottingFunction in PlottingAlgorithms.registeredAlgorithms.values():
                    if plottingFunction.computeOnClick:
                        self._plotterPresenter.setOriginalImageDataAsDirty(plottingFunction.name)
                        self._plotterPresenter.setProcessedImageDataAsDirty(plottingFunction.name)

                if self._plotterPresenter.isVisible:
                    self._plotterPresenter.refresh()

        elif mouseButton == QtCore.Qt.RightButton:
            self._addRightClickPosition(clickPosition)

    def _addRightClickPosition(self, clickPosition):
        self._model.rightClickLastPositions.append(clickPosition)
        self._mainWindowPresenter.highlightImageLabelRightClickLastPositions(self._model.rightClickLastPositions)

    def _clearRightClickLastPositions(self):
        self._model.rightClickLastPositions.clear()
        self._mainWindowPresenter.highlightImageLabelRightClickLastPositions(None)

    def _getMagnifiedRegions(self, clickPosition):
        """
        # TODO: document MainPresenter._getMagnifiedRegions
        :param clickPosition: Utils.Point
        :return:
        """
        originalImagePixels = self._getMagnifiedRegion(self._model.originalImage, clickPosition)
        processedImagePixels = self._getMagnifiedRegion(self._model.processedImage, clickPosition)
        return originalImagePixels, processedImagePixels

    def _getMagnifiedRegion(self, image, clickPosition):
        """
        # TODO: document MainPresenter._getMagnifiedRegions
        Should explain what the function does here.
        :param clickPosition: Utils.Point
        :return:
        """
        frameGridSize = Application.Settings.MagnifierWindowSettings.gridSize

        imagePixels = numpy.full((frameGridSize, frameGridSize), None)

        if image is not None:
            if len(image.shape) == 3:
                imagePixels = numpy.full((frameGridSize, frameGridSize, image.shape[2]), None)

            frameOffset = frameGridSize // 2

            startIndexes = lambda pos, offset: (pos - offset, 0) if pos - offset >= 0 else (0, offset - pos)
            rowStartIndex, startEmptyRows = startIndexes(clickPosition.y, frameOffset)
            columnStartIndex, startEmptyColumns = startIndexes(clickPosition.x, frameOffset)

            endIndexes = lambda pos, offset, gridSize, imageSize: \
                (pos + offset + 1, gridSize) if pos + offset + 1 <= imageSize else (imageSize, offset + imageSize - pos)
            rowEndIndex, endFullRows = endIndexes(clickPosition.y, frameOffset, frameGridSize, image.shape[0])
            columnEndIndex, endFullColumns = endIndexes(clickPosition.x, frameOffset, frameGridSize, image.shape[1])

            imagePixels[startEmptyRows:endFullRows, startEmptyColumns:endFullColumns] = \
                image[rowStartIndex:rowEndIndex, columnStartIndex:columnEndIndex]

        return imagePixels

    def resetPresenters(self):
        self._magnifierPresenter.clear()
        self._plotterPresenter.reset()
        self._mainWindowPresenter.reset()
