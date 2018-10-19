from Application.Model import Model
from Application.View import MagnifierWindow, MainWindow, PlotterWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2 as opencv
import numpy
import Application.Settings


class Controller(QtCore.QObject):

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
        self.mainWindow.rightMenuBar.addAction('Save as original image', self.__actionSaveAsOriginalImage)

        # connect the actions to methods
        self.mainWindow.actionExit.triggered.connect(self.__actionExit)
        self.mainWindow.actionInvert.triggered.connect(self.__actionInvert)
        self.mainWindow.actionLoadColorImage.triggered.connect(self.__actionLoadColorImage)
        self.mainWindow.actionLoadGrayscaleImage.triggered.connect(self.__actionLoadGrayscaleImage)
        self.mainWindow.actionMagnifier.triggered.connect(self.__actionMagnifier)
        self.mainWindow.actionPlotter.triggered.connect(self.__actionPlotter)
        self.mainWindow.actionSaveProcessedImage.triggered.connect(self.__actionSaveProcessedImage)

        # connect image labels to slots for updating the ui
        self.mainWindow.labelOriginalImageOverlay.mouse_moved.connect(self.__mouseMovedEvent)
        self.mainWindow.labelProcessedImageOverlay.mouse_moved.connect(self.__mouseMovedEvent)
        self.mainWindow.labelOriginalImageOverlay.mouse_pressed.connect(self.__mousePressedEvent)
        self.mainWindow.labelProcessedImageOverlay.mouse_pressed.connect(self.__mousePressedEvent)

        # connect the zoom option
        self.mainWindow.horizontalSliderZoom.valueChanged.connect(self.__zoomValueChangedEvent)
        self.mainWindow.buttonResetZoom.pressed.connect(self.__zoomValueResetEvent)

        # add options for the magnifier
        self.magnifierWindow.comboBoxColorSpace.addItems([item.value[1] for item in Application.Settings.MagnifierWindowSettings.ColorSpaces])
        self.magnifierWindow.comboBoxColorSpace.currentIndexChanged.connect(self.__magnifierColorSpaceIndexChanged)
        self.magnifierWindow.closing.connect(self.__magnifierWindowClosed)
        self.magnifierWindow.showing.connect(self.__magnifierWindowShowed)
        self.__isMagnifierWindowShowing = False
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
        self.plotterWindow.comboBoxFunction.currentIndexChanged.connect(self.__plotterFunctionIndexChanged)
        self.__lastClick = None
        self.plotterWindow.closing.connect(self.__plotterWindowClosed)
        self.plotterWindow.showing.connect(self.__plotterWindowShowed)
        self.__isPlotterWindowShowing = False

        # show the main window
        self.mainWindow.show()

    def __actionExit(self):
        QtCore.QCoreApplication.quit()

    def __actionInvert(self):
        self.model.processedImage = numpy.invert(self.model.originalImage)
        self.__setImages(processedImage=self.model.processedImage, originalImage=self.model.originalImage)

    def __actionLoadColorImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.mainWindow, caption='Open color file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
                                                            )

        self.model.loadOriginalImage(filename, opencv.IMREAD_COLOR)
        self.mainWindow.setImages(originalImage=self.model.originalImage, processedImage=None)

        self.model.processedImage = None

        self.__setMagnifierColorSpace(Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB)
        self.__resetApplicationState()

    def __actionLoadGrayscaleImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.mainWindow, caption='Open grayscale file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
                                                            )

        self.model.loadOriginalImage(filename, opencv.IMREAD_GRAYSCALE)
        self.mainWindow.setImages(originalImage=self.model.originalImage, processedImage=None)

        self.model.processedImage = None

        self.__setMagnifierColorSpace(Application.Settings.MagnifierWindowSettings.ColorSpaces.GRAY)
        self.__resetApplicationState()

    def __actionMagnifier(self):
        self.magnifierWindow.show()

    def __actionPlotter(self):
        self.plotterWindow.show()

    def __actionSaveAsOriginalImage(self):
        self.model.originalImage = self.model.processedImage
        self.model.processedImage = None
        self.__setImages(originalImage=self.model.originalImage, processedImage=None)

        if self.model.originalImage is None:
            self.__resetApplicationState()

        self.__setClickPosition()

    def __actionSaveProcessedImage(self):
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

    def __mouseMovedEvent(self, QMouseEvent):
        # TODO: take zoom into account
        x = QMouseEvent.x()
        y = QMouseEvent.y()

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

    def __mousePressedEvent(self, QMouseEvent):
        if self.__isMagnifierWindowShowing or self.__isPlotterWindowShowing:
            # TODO: take zoom into account
            self.__lastClick = QMouseEvent.pos()

            # show the click point on the main window label
            self.__setClickPosition()

            # calculate the parameters for the magnifier window
            self.__calculateAndSetMagnifierParameters()

            # calculate the parameters for the plotter window
            self.__calculateAndSetPlotterParameters()

    def __plotterFunctionIndexChanged(self, index):
        self.__calculateAndSetPlotterParameters()

    def __calculateAndSetPlotterParameters(self):
        plotItemOriginalImage = self.plotterWindow.graphicsViewOriginalImage.getPlotItem()
        plotItemProcessedImage = self.plotterWindow.graphicsViewProcessedImage.getPlotItem()
        # TODO: rethink this part to be easily usable and editable by others
        self.plotterWindow.reset()

        plotDataItemOriginalImage = None
        plotDataItemProcessedImage = None
        plotDataItems = []

        if self.__lastClick is not None:
            if self.plotterWindow.comboBoxFunction.currentIndex() == Application.Settings.PlotterWindowSettings.Functions.PLOT_COL_GRAY_VALUES.value[0]:
                if self.model.originalImage is not None and len(self.model.originalImage.shape) == 2:
                    plotDataItemOriginalImage = plotItemOriginalImage.plot(range(self.model.originalImage.shape[1]),
                                  self.model.originalImage[self.__lastClick.y()],
                                  pen=QtGui.QColor(QtCore.Qt.red),
                                  name='Original image')
                    self.plotterWindow.plotLegendStringList.append('Original image')
                if self.model.processedImage is not None and len(self.model.originalImage.shape) == 2:
                    plotDataItemProcessedImage = plotItemProcessedImage.plot(range(self.model.processedImage.shape[1]),
                                  self.model.processedImage[self.__lastClick.y()],
                                  pen=QtGui.QColor(QtCore.Qt.green),
                                  name='Processed image')
                    self.plotterWindow.plotLegendStringList.append('Processed image')
            elif self.plotterWindow.comboBoxFunction.currentIndex() == Application.Settings.PlotterWindowSettings.Functions.PLOT_ROW_GRAY_VALUES.value[0]:
                if self.model.originalImage is not None and len(self.model.originalImage.shape) == 2:
                    plotDataItemOriginalImage = plotItemOriginalImage.plot(range(self.model.originalImage.shape[0]),
                                  self.model.originalImage[:, self.__lastClick.x()],
                                  pen=QtGui.QColor(QtCore.Qt.red),
                                  name='Original image')
                    self.plotterWindow.plotLegendStringList.append('Original image')
                if self.model.processedImage is not None and len(self.model.originalImage.shape) == 2:
                    plotDataItemProcessedImage = plotItemProcessedImage.plot(range(self.model.processedImage.shape[0]),
                                  self.model.processedImage[:, self.__lastClick.x()],
                                  pen=QtGui.QColor(QtCore.Qt.green),
                                  name='Processed image')
                    self.plotterWindow.plotLegendStringList.append('Processed image')

        if plotDataItemOriginalImage is not None:
            plotDataItems.append(plotDataItemOriginalImage)

        if plotDataItemProcessedImage is not None:
            plotDataItems.append(plotDataItemProcessedImage)

        plotItemOriginalImage.getViewBox().autoRange(items=plotDataItems)
        plotItemProcessedImage.getViewBox().autoRange(items=plotDataItems)

    def __setMagnifierColorSpace(self, colorSpace : Application.Settings.MagnifierWindowSettings.ColorSpaces):
        self.magnifierWindow.comboBoxColorSpace.setCurrentIndex(colorSpace.value[0])

        for row in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
            for column in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
                self.magnifierWindow.frameListOriginalImage[row][column].setColorDisplayFormat(colorSpace)
                self.magnifierWindow.frameListProcessedImage[row][column].setColorDisplayFormat(colorSpace)

    def __magnifierColorSpaceIndexChanged(self, index):
        displayFormat = None

        if index == Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB
        elif index == Application.Settings.MagnifierWindowSettings.ColorSpaces.HSL.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorSpaces.HSL
        elif index == Application.Settings.MagnifierWindowSettings.ColorSpaces.HSV.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorSpaces.HSV
        elif index == Application.Settings.MagnifierWindowSettings.ColorSpaces.CMYK.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorSpaces.CMYK
        elif index == Application.Settings.MagnifierWindowSettings.ColorSpaces.GRAY.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorSpaces.GRAY

        self.__setMagnifierColorSpace(displayFormat)

    def __calculateAndSetMagnifierParameters(self):
        if self.__lastClick is not None:
            offset = Application.Settings.MagnifierWindowSettings.frameGridSize // 2

            for row in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
                for column in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
                    yPos = self.__lastClick.y() - offset + row
                    xPos = self.__lastClick.x() - offset + column

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

    def __setImages(self, originalImage, processedImage):
        self.mainWindow.setImages(processedImage=processedImage, originalImage=originalImage)

        if self.__isMagnifierWindowShowing or self.__isPlotterWindowShowing:
            self.__calculateAndSetMagnifierParameters()
            self.__calculateAndSetPlotterParameters()

        self.__setClickPosition()

    def __zoomValueResetEvent(self):
        # TODO: get rid of magic numbers here, use the settings class
        self.mainWindow.horizontalSliderZoom.setValue(18)
        self.__zoomValueChangedEvent(18)

    def __zoomValueChangedEvent(self, value):
        zoom = self.__calculateZoomFromSliderValue(value)
        self.__setZoom(zoom)
        self.mainWindow.labelZoomFactor.setText(f"{zoom:.2f}x")

    def __calculateZoomFromSliderValue(self, value):
        # slider goes from 0 to 198, in steps of 1
        # zoom goes from 0.1x to 10x in steps of 0.1
        # TODO: get rid of magic numbers here, use the settings class
        return value * 0.05 + 0.1

    def __setZoom(self, zoom):
        self.mainWindow.labelOriginalImage.setZoom(zoom)
        self.mainWindow.labelProcessedImage.setZoom(zoom)
        self.mainWindow.labelOriginalImageOverlay.setZoom(zoom)
        self.mainWindow.labelProcessedImageOverlay.setZoom(zoom)

    def __resetApplicationState(self):
        self.magnifierWindow.reset()
        self.plotterWindow.reset()
        self.mainWindow.labelOriginalImageOverlay.setClickPosition(None)
        self.mainWindow.labelProcessedImageOverlay.setClickPosition(None)
        self.__lastClick = None

    def __magnifierWindowShowed(self):
        self.__isMagnifierWindowShowing = True

    def __magnifierWindowClosed(self):
        self.__isMagnifierWindowShowing = False

        if not self.__isPlotterWindowShowing:
            self.__resetApplicationState()

    def __plotterWindowShowed(self):
        self.__isPlotterWindowShowing = True

    def __plotterWindowClosed(self):
        self.__isPlotterWindowShowing = False

        if not self.__isMagnifierWindowShowing:
            self.__resetApplicationState()

    def __setClickPosition(self):
        self.mainWindow.labelOriginalImageOverlay.setClickPosition(None)
        self.mainWindow.labelProcessedImageOverlay.setClickPosition(None)

        if self.__isPlotterWindowShowing or self.__isMagnifierWindowShowing:
            if self.model.originalImage is not None:
                self.mainWindow.labelOriginalImageOverlay.setClickPosition(self.__lastClick)

            if self.model.processedImage is not None:
                self.mainWindow.labelProcessedImageOverlay.setClickPosition(self.__lastClick)
