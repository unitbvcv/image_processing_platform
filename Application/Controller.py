from Application.Model import Model
from Application.View import MagnifierWindow, MainWindow, PlotterWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2 as opencv
import numpy
import Application.Settings


class Controller(QtCore.QObject):
    _isMagnifierWindowShowing = False
    _isPlotterWindowShowing = False

    def __init__(self, parent=None):
        super().__init__(parent)
        # instantiate the model
        self.model = Model()

        # instantiate the QMainWindow objects
        self.mainWindow = MainWindow()
        self.plotterWindow = PlotterWindow(self.mainWindow)
        self.magnifierWindow = MagnifierWindow(self.mainWindow)

        # create menubar option for saving as original image in the right side
        # it can't be put in the UI init class because rightMenuBar's addAction method doesn't take a QAction object
        self.mainWindow.rightMenuBar = QtWidgets.QMenuBar()
        self.mainWindow.menuBar.setCornerWidget(self.mainWindow.rightMenuBar)
        self.mainWindow.rightMenuBar.addAction('Save as original image', self._actionSaveAsOriginalImage)

        # connect the actions to methods
        self.mainWindow.actionExit.triggered.connect(self._actionExit)
        self.mainWindow.actionInvert.triggered.connect(self._actionInvert)
        self.mainWindow.actionLoadColorImage.triggered.connect(self._actionLoadColorImage)
        self.mainWindow.actionLoadGrayscaleImage.triggered.connect(self._actionLoadGrayscaleImage)
        self.mainWindow.actionMagnifier.triggered.connect(self._actionMagnifier)
        self.mainWindow.actionPlotter.triggered.connect(self._actionPlotter)
        self.mainWindow.actionSaveProcessedImage.triggered.connect(self._actionSaveProcessedImage)

        # connect image labels to slots for updating the ui
        self.mainWindow.labelOriginalImage.mouse_moved.connect(self._mouseMovedEvent)
        self.mainWindow.labelProcessedImage.mouse_moved.connect(self._mouseMovedEvent)
        self.mainWindow.labelOriginalImage.mouse_pressed.connect(self._mousePressedEvent)
        self.mainWindow.labelProcessedImage.mouse_pressed.connect(self._mousePressedEvent)
        self.mainWindow.labelOriginalImage.mouse_leaved.connect(self._mouseLeavedEvent)
        self.mainWindow.labelProcessedImage.mouse_leaved.connect(self._mouseLeavedEvent)
        self.mainWindow.labelOriginalImage.finished_painting.connect(self._labelFinishedPaintingEvent)
        self.mainWindow.labelProcessedImage.finished_painting.connect(self._labelFinishedPaintingEvent)

        # connect the zoom option
        self.mainWindow.horizontalSliderZoom.setMinimum(
            self._calculateSliderValueFromZoom(Application.Settings.MainWindowSettings.zoomMinimumValue))
        self.mainWindow.horizontalSliderZoom.setMaximum(
            self._calculateSliderValueFromZoom(Application.Settings.MainWindowSettings.zoomMaximumValue))
        self.mainWindow.horizontalSliderZoom.setSingleStep(
            self._calculateSliderValueFromZoom(Application.Settings.MainWindowSettings.zoomSingleStep))
        self.mainWindow.horizontalSliderZoom.setPageStep(
            self._calculateSliderValueFromZoom(Application.Settings.MainWindowSettings.zoomPageStep))
        self.mainWindow.horizontalSliderZoom.setTickInterval(
            self._calculateSliderValueFromZoom(Application.Settings.MainWindowSettings.ticksInterval)
        )
        defaultZoom = self._calculateSliderValueFromZoom(Application.Settings.MainWindowSettings.zoomDefaultValue)
        self.mainWindow.horizontalSliderZoom.setValue(defaultZoom)
        self.mainWindow.horizontalSliderZoom.valueChanged.connect(self._zoomValueChangedEvent)
        self.mainWindow.buttonResetZoom.pressed.connect(self._zoomValueResetEvent)
        self._zoom = self._calculateSliderValueFromZoom(defaultZoom)

        # add options for the magnifier
        self.magnifierWindow.comboBoxColorModel.addItems([item.value[1] for item in Application.Settings.MagnifierWindowSettings.ColorModels])
        self.magnifierWindow.comboBoxColorModel.currentIndexChanged.connect(self._magnifierColorModelIndexChanged)
        self.magnifierWindow.closing.connect(self._magnifierWindowClosed)
        self.magnifierWindow.showing.connect(self._magnifierWindowShowed)

        # validate magnifier settings
        assert (Application.Settings.MagnifierWindowSettings.frameGridSize % 2 == 1)
        assert (Application.Settings.MagnifierWindowSettings.frameGridSize > 0)
        assert (Application.Settings.MagnifierWindowSettings.fontSize > 0)

        # add options for the plotter
        self.plotterWindow.comboBoxFunction.addItems([item.value[1] for item in Application.Settings.PlotterWindowSettings.Functions])
        plotItemOriginalImage = self.plotterWindow.graphicsViewOriginalImage.getPlotItem()
        plotItemProcessedImage = self.plotterWindow.graphicsViewProcessedImage.getPlotItem()
        plotItemOriginalImage.setMenuEnabled(False)
        plotItemProcessedImage.setMenuEnabled(False)
        plotItemOriginalImage.addLegend()
        plotItemProcessedImage.addLegend()
        plotItemOriginalImage.showGrid(x=True, y=True, alpha=1.0)
        plotItemProcessedImage.showGrid(x=True, y=True, alpha=1.0)
        self.plotterWindow.graphicsViewOriginalImage.setXLink(self.plotterWindow.graphicsViewProcessedImage)
        self.plotterWindow.graphicsViewOriginalImage.setYLink(self.plotterWindow.graphicsViewProcessedImage)
        self.plotterWindow.comboBoxFunction.currentIndexChanged.connect(self._plotterFunctionIndexChanged)
        self._lastClick = None
        self.plotterWindow.closing.connect(self._plotterWindowClosed)
        self.plotterWindow.showing.connect(self._plotterWindowShowed)

        # show the main window
        self.mainWindow.show()

    def _actionExit(self):
        """
        test
        :return:
        """
        QtCore.QCoreApplication.quit()

    def _actionInvert(self):
        if self.model.originalImage is not None:
            self.model.processedImage = numpy.invert(self.model.originalImage)

            # UI code, independent of algorithm
            self._setImages(processedImage=self.model.processedImage, originalImage=self.model.originalImage)

    def _actionLoadColorImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.mainWindow, caption='Open color file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
                                                            )

        self.model.loadOriginalImage(filename, opencv.IMREAD_COLOR)
        self.mainWindow.setImages(originalImage=self.model.originalImage, processedImage=None)

        self.model.processedImage = None

        self._setMagnifierColorModel(Application.Settings.MagnifierWindowSettings.ColorModels.RGB)
        self._resetApplicationState()

    def _actionLoadGrayscaleImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.mainWindow, caption='Open grayscale file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
                                                            )

        self.model.loadOriginalImage(filename, opencv.IMREAD_GRAYSCALE)
        self.mainWindow.setImages(originalImage=self.model.originalImage, processedImage=None)

        self.model.processedImage = None

        self._setMagnifierColorModel(Application.Settings.MagnifierWindowSettings.ColorModels.GRAY)
        self._resetApplicationState()

    def _actionMagnifier(self):
        self.magnifierWindow.show()

    def _actionPlotter(self):
        self.plotterWindow.show()

    def _actionSaveAsOriginalImage(self):
        self.model.originalImage = self.model.processedImage
        self.model.processedImage = None
        self._setImages(originalImage=self.model.originalImage, processedImage=None)

        if self.model.originalImage is None:
            self._resetApplicationState()

        self._setClickPosition()

    def _actionSaveProcessedImage(self):
        if self.model.processedImage is not None:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(parent=self.mainWindow, caption='Save processed image',
                                                                filter='Bitmap file (*.bmp *.dib);;'
                                                                       'JPEG file (*.jpeg *.jpg *.jpe);;'
                                                                       'JPEG 2000 file (*.jp2);;'
                                                                       'Portable Network Graphics file (*.png);;'
                                                                       'WebP file (*.webp);;'
                                                                       'Sun rasters file (*.ras *.sr);;'
                                                                       'Tagged Image file (*.tiff *.tif)',
                                                                initialFilter='Portable Network Graphics file (*.png)'
                                                                )

            opencv.imwrite(filename, self.model.processedImage)

    def _mouseMovedEvent(self, QMouseEvent):
        if self._zoom != 0:
            x = int(QMouseEvent.x() / self._zoom)
            y = int(QMouseEvent.y() / self._zoom)

            labelText = ''

            # updating pixel position label
            senderImageLabel = self.sender()
            if senderImageLabel == self.mainWindow.labelOriginalImage:
                if self.model.originalImage is not None:
                    labelText = f'Mouse position: (X, Y) = ({x}, {y})'
            elif senderImageLabel == self.mainWindow.labelProcessedImage:
                if self.model.processedImage is not None:
                    labelText = f'Mouse position: (X, Y) = ({x}, {y})'
            self.mainWindow.labelMousePosition.setText(labelText)

            labelText = ''

            # updating original image pixel label
            if self.model.originalImage is not None:
                if len(self.model.originalImage.shape) == 3:
                    pixel = self.model.originalImage[y][x]
                    labelText = f'(R, G, B) = ({pixel[2]}, {pixel[1]}, {pixel[0]})'
                elif len(self.model.originalImage.shape) == 2:
                    pixel = self.model.originalImage[y][x]
                    labelText = f'(Gray) = ({pixel})'
            self.mainWindow.labelOriginalImagePixelValue.setText(labelText)

            labelText = ''

            # updating processed image pixel label
            if self.model.processedImage is not None:
                if len(self.model.processedImage.shape) == 3:
                    pixel = self.model.processedImage[y][x]
                    labelText = f'(R, G, B) = ({pixel[2]}, {pixel[1]}, {pixel[0]})'
                elif len(self.model.processedImage.shape) == 2:
                    pixel = self.model.processedImage[y][x]
                    labelText = f'(Gray) = ({pixel})'
            self.mainWindow.labelProcessedImagePixelValue.setText(labelText)

    def _mousePressedEvent(self, QMouseEvent):
        if self._isMagnifierWindowShowing or self._isPlotterWindowShowing:
            if self._zoom != 0:
                self._lastClick = (QMouseEvent.pos() / self._zoom)

                # show the click point on the main window label
                self._setClickPosition()

                # calculate the parameters for the magnifier window
                self._calculateAndSetMagnifierParameters()

                # calculate the parameters for the plotter window
                self._calculateAndSetPlotterParameters()

    def _mouseLeavedEvent(self, QEvent):
        self.mainWindow.labelMousePosition.setText('')
        self.mainWindow.labelOriginalImagePixelValue.setText('')
        self.mainWindow.labelProcessedImagePixelValue.setText('')

    def _plotterFunctionIndexChanged(self, index):
        self._calculateAndSetPlotterParameters()

    def _calculateAndSetPlotterParameters(self):
        plotItemOriginalImage = self.plotterWindow.graphicsViewOriginalImage.getPlotItem()
        plotItemProcessedImage = self.plotterWindow.graphicsViewProcessedImage.getPlotItem()
        # TODO: rethink this part to be easily usable and editable by others
        self.plotterWindow.reset()

        plotDataItemOriginalImage = None
        plotDataItemProcessedImage = None
        plotDataItems = []

        if self._lastClick is not None:
            if self.plotterWindow.comboBoxFunction.currentIndex() == Application.Settings.PlotterWindowSettings.Functions.PLOT_ROW_GRAY_VALUES.value[0]:
                if self.model.originalImage is not None and len(self.model.originalImage.shape) == 2:
                    plotDataItemOriginalImage = plotItemOriginalImage.plot(range(self.model.originalImage.shape[1]),
                                  self.model.originalImage[self._lastClick.y()],
                                  pen=QtGui.QColor(QtCore.Qt.red),
                                  name='Original image')
                    self.plotterWindow.plotLegendStringList.append('Original image')
                if self.model.processedImage is not None and len(self.model.originalImage.shape) == 2:
                    plotDataItemProcessedImage = plotItemProcessedImage.plot(range(self.model.processedImage.shape[1]),
                                  self.model.processedImage[self._lastClick.y()],
                                  pen=QtGui.QColor(QtCore.Qt.green),
                                  name='Processed image')
                    self.plotterWindow.plotLegendStringList.append('Processed image')
            elif self.plotterWindow.comboBoxFunction.currentIndex() == Application.Settings.PlotterWindowSettings.Functions.PLOT_COL_GRAY_VALUES.value[0]:
                if self.model.originalImage is not None and len(self.model.originalImage.shape) == 2:
                    plotDataItemOriginalImage = plotItemOriginalImage.plot(range(self.model.originalImage.shape[0]),
                                  self.model.originalImage[:, self._lastClick.x()],
                                  pen=QtGui.QColor(QtCore.Qt.red),
                                  name='Original image')
                    self.plotterWindow.plotLegendStringList.append('Original image')
                if self.model.processedImage is not None and len(self.model.originalImage.shape) == 2:
                    plotDataItemProcessedImage = plotItemProcessedImage.plot(range(self.model.processedImage.shape[0]),
                                  self.model.processedImage[:, self._lastClick.x()],
                                  pen=QtGui.QColor(QtCore.Qt.green),
                                  name='Processed image')
                    self.plotterWindow.plotLegendStringList.append('Processed image')

        if plotDataItemOriginalImage is not None:
            plotDataItems.append(plotDataItemOriginalImage)

        if plotDataItemProcessedImage is not None:
            plotDataItems.append(plotDataItemProcessedImage)

        plotItemOriginalImage.getViewBox().autoRange(items=plotDataItems)
        plotItemProcessedImage.getViewBox().autoRange(items=plotDataItems)

    def _setMagnifierColorModel(self, colorModel : Application.Settings.MagnifierWindowSettings.ColorModels):
        self.magnifierWindow.comboBoxColorModel.setCurrentIndex(colorModel.value[0])

        for row in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
            for column in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
                self.magnifierWindow.frameListOriginalImage[row][column].setColorDisplayFormat(colorModel)
                self.magnifierWindow.frameListProcessedImage[row][column].setColorDisplayFormat(colorModel)

    def _magnifierColorModelIndexChanged(self, index):
        displayFormat = None

        if index == Application.Settings.MagnifierWindowSettings.ColorModels.RGB.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorModels.RGB
        elif index == Application.Settings.MagnifierWindowSettings.ColorModels.HSL.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorModels.HSL
        elif index == Application.Settings.MagnifierWindowSettings.ColorModels.HSV.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorModels.HSV
        elif index == Application.Settings.MagnifierWindowSettings.ColorModels.CMYK.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorModels.CMYK
        elif index == Application.Settings.MagnifierWindowSettings.ColorModels.GRAY.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorModels.GRAY

        self._setMagnifierColorModel(displayFormat)

    def _calculateAndSetMagnifierParameters(self):
        if self._lastClick is not None:
            offset = Application.Settings.MagnifierWindowSettings.frameGridSize // 2

            for row in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
                for column in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
                    yPos = self._lastClick.y() - offset + row
                    xPos = self._lastClick.x() - offset + column

                    if self.model.originalImage is not None and yPos >= 0 and xPos >= 0 and \
                            yPos < self.model.originalImage.shape[0] and xPos < self.model.originalImage.shape[1]:
                        pixelOriginalImage = self.model.originalImage[yPos, xPos]
                    else:
                        pixelOriginalImage = None

                    if self.model.processedImage is not None and yPos >= 0 and xPos >= 0 and \
                            yPos < self.model.processedImage.shape[0] and xPos < self.model.processedImage.shape[1]:
                        pixelProcessedImage = self.model.processedImage[yPos, xPos]
                    else:
                        pixelProcessedImage = None

                    if pixelOriginalImage is not None:
                        if len(self.model.originalImage.shape) == 3:
                            self.magnifierWindow.frameListOriginalImage[row][column].setFrameColorRgb(pixelOriginalImage[2],
                                                                                                      pixelOriginalImage[1],
                                                                                                      pixelOriginalImage[0])
                        elif len(self.model.originalImage.shape) == 2:
                            self.magnifierWindow.frameListOriginalImage[row][column].setFrameColorGrayLevel(
                                pixelOriginalImage)
                    else:
                        self.magnifierWindow.frameListOriginalImage[row][column].setFrameColorGrayLevel(None)

                    if pixelProcessedImage is not None:
                        if len(self.model.processedImage.shape) == 3:
                            self.magnifierWindow.frameListProcessedImage[row][column].setFrameColorRgb(
                                pixelProcessedImage[2], pixelProcessedImage[1], pixelProcessedImage[0])
                        elif len(self.model.originalImage.shape) == 2:
                            self.magnifierWindow.frameListProcessedImage[row][column].setFrameColorGrayLevel(
                                pixelProcessedImage)
                    else:
                        self.magnifierWindow.frameListProcessedImage[row][column].setFrameColorGrayLevel(None)

    def _setImages(self, originalImage, processedImage):
        self.mainWindow.setImages(processedImage=processedImage, originalImage=originalImage)

        # resetting the images will show them with original resolution
        # they need to be zoomed
        self._zoomValueChangedEvent(self._calculateSliderValueFromZoom(self._zoom))

        if self._isMagnifierWindowShowing or self._isPlotterWindowShowing:
            self._calculateAndSetMagnifierParameters()
            self._calculateAndSetPlotterParameters()

        self._setClickPosition()

    def _zoomValueResetEvent(self):
        sliderValue = self._calculateSliderValueFromZoom(Application.Settings.MainWindowSettings.zoomDefaultValue)
        self.mainWindow.horizontalSliderZoom.setValue(sliderValue)
        self._zoomValueChangedEvent(sliderValue)

    def _zoomValueChangedEvent(self, value):
        self._zoom = self._calculateZoomFromSliderValue(value)
        self.mainWindow.labelZoomFactor.setText(f"{self._zoom:.2f}x")
        self._setZoomInView()

    def _calculateZoomFromSliderValue(self, value):
        return value * Application.Settings.MainWindowSettings.zoomSingleStep \
               + Application.Settings.MainWindowSettings.zoomMinimumValue

    def _calculateSliderValueFromZoom(self, value):
        return int((value - Application.Settings.MainWindowSettings.zoomMinimumValue)
                   / Application.Settings.MainWindowSettings.zoomSingleStep)

    def _setZoomInView(self):
        self.mainWindow.labelOriginalImage.setZoom(self._zoom)
        self.mainWindow.labelProcessedImage.setZoom(self._zoom)
        self._setClickPosition()

    def _resetApplicationState(self):
        self.magnifierWindow.reset()
        self.plotterWindow.reset()
        self.mainWindow.labelOriginalImage.setClickPosition(None)
        self.mainWindow.labelProcessedImage.setClickPosition(None)
        self._lastClick = None
        self._zoomValueResetEvent()
        self.mainWindow.scrollAreaOriginalImage.horizontalScrollBar().setValue(0)

    def _magnifierWindowShowed(self):
        self._isMagnifierWindowShowing = True

    def _magnifierWindowClosed(self):
        self._isMagnifierWindowShowing = False

        if not self._isPlotterWindowShowing:
            self._resetApplicationState()

    def _plotterWindowShowed(self):
        self._isPlotterWindowShowing = True

    def _plotterWindowClosed(self):
        self._isPlotterWindowShowing = False

        if not self._isMagnifierWindowShowing:
            self._resetApplicationState()

    def _setClickPosition(self):
        self.mainWindow.labelOriginalImage.setClickPosition(None)
        self.mainWindow.labelProcessedImage.setClickPosition(None)

        if self._isPlotterWindowShowing or self._isMagnifierWindowShowing:
            if self.model.originalImage is not None:
                self.mainWindow.labelOriginalImage.setClickPosition(self._lastClick)

            if self.model.processedImage is not None:
                self.mainWindow.labelProcessedImage.setClickPosition(self._lastClick)

    def _labelFinishedPaintingEvent(self):
        # here we can synchronize scrollbars, after the paint event has finished
        # before paint event, the scrollbars don't exist
        self.mainWindow.scrollAreaProcessedImage.horizontalScrollBar().setValue(
            self.mainWindow.scrollAreaOriginalImage.horizontalScrollBar().value())

        self.mainWindow.scrollAreaProcessedImage.verticalScrollBar().setValue(
            self.mainWindow.scrollAreaOriginalImage.verticalScrollBar().value())
