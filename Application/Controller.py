from Application.Model import Model
from Application.View import MagnifierWindow, MainWindow, PlotterWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2 as opencv
import numpy


class Controller(object):

    def __init__(self):
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

    def __actionLoadGrayscaleImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.mainWindow, caption='Open grayscale file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
                                                            )

        self.model.loadOriginalImage(filename, opencv.IMREAD_GRAYSCALE)
        self.mainWindow.setImages(originalImage=self.model.originalImage, processedImage=None)

        self.model.processedImage = None

    def __actionMagnifier(self):
        # TODO
        self.magnifierWindow.show()

    def __actionPlotter(self):
        # TODO
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

        # updating original image pixel label
        if self.mainWindow.labelOriginalImage.pixmap() is not None and self.model.originalImage is not None:
            if len(self.model.originalImage.shape) == 3:
                pass
            elif len(self.model.originalImage.shape) == 2:
                pass

        # updating processed image pixel label
        if self.mainWindow.labelOriginalImage.pixmap() is not None and self.model.processedImage is not None:
            if len(self.model.processedImage.shape) == 3:
                pass
            elif len(self.model.processedImage.shape) == 2:
                pass

    def __mousePressedEvent(self, QMouseEvent):

        if self.magnifierWindow.isVisible():
            rows = len(self.magnifierWindow.frameListOriginalImage)
            columns = len(self.magnifierWindow.frameListOriginalImage[0])

            for row in range(rows):
                for column in range(columns):
                    if self.model.originalImage is not None:
                        pixelOriginalImage = self.model.originalImage[QMouseEvent.y() - column // 2, QMouseEvent.x() - row // 2]
                    else:
                        pixelOriginalImage = None

                    if self.model.processedImage is not None:
                        pixelProcessedImage = self.model.processedImage[QMouseEvent.y() - columns//2, QMouseEvent.x() - row // 2]
                    else:
                        pixelProcessedImage = None

                    frameRectOriginalImage = self.magnifierWindow.frameListOriginalImage[row][column].rect()
                    frameRectProcessedImage = self.magnifierWindow.frameListProcessedImage[row][column].rect()

                    painterOriginalImage = QtGui.QPainter(self.magnifierWindow.frameListOriginalImage[row][column])
                    painterProcessedImage = QtGui.QPainter(self.magnifierWindow.frameListProcessedImage[row][column])

                    if pixelOriginalImage is None:
                        painterOriginalImage.eraseRect(frameRectOriginalImage)
                    else:
                        if pixelOriginalImage.shape == 3:
                            painterOriginalImage.fillRect(frameRectOriginalImage, QtGui.QColor(pixelOriginalImage[2], pixelOriginalImage[1], pixelOriginalImage[0]))
                        elif pixelOriginalImage.shape == 1:
                            painterOriginalImage.fillRect(frameRectOriginalImage, QtGui.QColor(pixelOriginalImage[0], pixelOriginalImage[0], pixelOriginalImage[0]))

                    if pixelProcessedImage is None:
                        painterProcessedImage.eraseRect(frameRectProcessedImage)
                    else:
                        if pixelProcessedImage.shape == 3:
                            painterProcessedImage.fillRect(frameRectProcessedImage, QtGui.QColor(pixelProcessedImage[2], pixelProcessedImage[1], pixelProcessedImage[0]))
                        elif pixelProcessedImage.shape == 1:
                            painterOriginalImage.fillRect(frameRectOriginalImage, QtGui.QColor(pixelProcessedImage[0], pixelProcessedImage[0], pixelProcessedImage[0]))

            self.magnifierWindow.repaint()
