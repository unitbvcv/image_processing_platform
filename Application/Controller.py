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
        self.mainWindow.labelOriginalImage.mouse_moved.connect(self.__mouseMovedEvent)
        self.mainWindow.labelProcessedImage.mouse_moved.connect(self.__mouseMovedEvent)
        self.mainWindow.labelOriginalImage.mouse_pressed.connect(self.__mousePressedEvent)
        self.mainWindow.labelProcessedImage.mouse_pressed.connect(self.__mousePressedEvent)

        # add options for the magnifier
        self.magnifierWindow.comboBoxColorSpace.addItems([item.value[1] for item in Application.Settings.MagnifierWindowSettings.ColorSpaces])
        self.magnifierWindow.comboBoxColorSpace.currentIndexChanged.connect(self.__magnifierColorSpaceIndexChanged)

        # add options for the plotter
        self.plotterWindow.comboBoxFunction.addItems([item.value[1] for item in Application.Settings.PlotterWindowSettings.Functions])
        plotItem = self.plotterWindow.graphicsView.getPlotItem()
        plotItem.setMenuEnabled(False)
        plotItem.addLegend()
        self.plotterWindow.comboBoxFunction.currentIndexChanged.connect(self.__plotterFunctionIndexChanged)
        self.__lastClick = None

        # show the main window
        self.mainWindow.show()

    def __actionExit(self):
        QtCore.QCoreApplication.quit()

    def __actionInvert(self):
        self.model.processedImage = numpy.invert(self.model.originalImage)
        self.mainWindow.setImages(processedImage=self.model.processedImage, originalImage=self.model.originalImage)

    def __actionLoadColorImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.mainWindow, caption='Open color file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
                                                            )

        self.model.loadOriginalImage(filename, opencv.IMREAD_COLOR)
        self.mainWindow.setImages(originalImage=self.model.originalImage, processedImage=None)

        self.model.processedImage = None

        self.__setMagnifierColorSpace(Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB)

    def __actionLoadGrayscaleImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.mainWindow, caption='Open grayscale file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
                                                            )

        self.model.loadOriginalImage(filename, opencv.IMREAD_GRAYSCALE)
        self.mainWindow.setImages(originalImage=self.model.originalImage, processedImage=None)

        self.model.processedImage = None

        self.__setMagnifierColorSpace(Application.Settings.MagnifierWindowSettings.ColorSpaces.GRAY)

    def __actionMagnifier(self):
        self.magnifierWindow.show()

    def __actionPlotter(self):
        self.plotterWindow.show()

    def __actionSaveAsOriginalImage(self):
        self.model.originalImage = self.model.processedImage
        self.model.processedImage = None
        self.mainWindow.setImages(originalImage=self.model.originalImage, processedImage=None)

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
        # show the click point on the main window label
        if self.model.originalImage is not None:
            self.mainWindow.labelOriginalImage.setClickPosition(QMouseEvent.pos())
        if self.model.processedImage is not None:
            self.mainWindow.labelProcessedImage.setClickPosition(QMouseEvent.pos())

        # calculate the parameters for the magnifier window
        offset = Application.Settings.MagnifierWindowSettings.frameGridSize // 2

        for row in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
            for column in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
                yPos = QMouseEvent.y() - offset + row
                xPos = QMouseEvent.x() - offset + column

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

                if self.model.originalImage is not None:
                    if len(self.model.originalImage.shape) == 3:
                        self.magnifierWindow.frameListOriginalImage[row][column].setFrameColorRgb(pixelOriginalImage[2], pixelOriginalImage[1], pixelOriginalImage[0])
                    elif len(self.model.originalImage.shape) == 2:
                        self.magnifierWindow.frameListOriginalImage[row][column].setFrameColorGrayLevel(pixelOriginalImage)
                else:
                    self.magnifierWindow.frameListOriginalImage[row][column].setFrameColorGrayLevel(None)

                if self.model.processedImage is not None:
                    if len(self.model.processedImage.shape) == 3:
                        self.magnifierWindow.frameListProcessedImage[row][column].setFrameColorRgb(pixelProcessedImage[2], pixelProcessedImage[1], pixelProcessedImage[0])
                    elif len(self.model.originalImage.shape) == 2:
                        self.magnifierWindow.frameListProcessedImage[row][column].setFrameColorGrayLevel(pixelProcessedImage)
                else:
                    self.magnifierWindow.frameListProcessedImage[row][column].setFrameColorGrayLevel(None)

        # calculate the parameters for the plotter window
        self.__lastClick = QMouseEvent.pos()
        self.__calculateAndSetPlotterParameters()

    def __plotterFunctionIndexChanged(self, index):
        self.__calculateAndSetPlotterParameters()

    def __calculateAndSetPlotterParameters(self):
        plotItem = self.plotterWindow.graphicsView.getPlotItem()
        # TODO: rethink this part to be easily usable and editable by others
        plotItem.clear()
        plotItem.legend.removeItem('Original image')
        plotItem.legend.removeItem('Processed image')

        if self.plotterWindow.comboBoxFunction.currentIndex() == Application.Settings.PlotterWindowSettings.Functions.PLOT_COL_GRAY_VALUES.value[0]:
            if self.model.originalImage is not None and len(self.model.originalImage.shape) == 2:
                plotItem.plot(range(self.model.originalImage.shape[1]),
                              self.model.originalImage[self.__lastClick.y()],
                              pen=QtGui.QColor(QtCore.Qt.red),
                              name='Original image')
            if self.model.processedImage is not None and len(self.model.originalImage.shape) == 2:
                plotItem.plot(range(self.model.processedImage.shape[1]),
                              self.model.processedImage[self.__lastClick.y()],
                              pen=QtGui.QColor(QtCore.Qt.green),
                              name='Processed image')
        elif self.plotterWindow.comboBoxFunction.currentIndex() == Application.Settings.PlotterWindowSettings.Functions.PLOT_ROW_GRAY_VALUES.value[0]:
            if self.model.originalImage is not None and len(self.model.originalImage.shape) == 2:
                plotItem.plot(range(self.model.originalImage.shape[0]),
                              self.model.originalImage[:, self.__lastClick.x()],
                              pen=QtGui.QColor(QtCore.Qt.red),
                              name='Original image')
            if self.model.processedImage is not None and len(self.model.originalImage.shape) == 2:
                plotItem.plot(range(self.model.processedImage.shape[0]),
                              self.model.processedImage[:, self.__lastClick.x()],
                              pen=QtGui.QColor(QtCore.Qt.green),
                              name='Processed image')

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
        if index == Application.Settings.MagnifierWindowSettings.ColorSpaces.HSL.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorSpaces.HSL
        if index == Application.Settings.MagnifierWindowSettings.ColorSpaces.HSV.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorSpaces.HSV
        if index == Application.Settings.MagnifierWindowSettings.ColorSpaces.CMYK.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorSpaces.CMYK
        if index == Application.Settings.MagnifierWindowSettings.ColorSpaces.GRAY.value[0]:
            displayFormat = Application.Settings.MagnifierWindowSettings.ColorSpaces.GRAY

        self.__setMagnifierColorSpace(displayFormat)
