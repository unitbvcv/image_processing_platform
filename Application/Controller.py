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
                                                  initialFilter='Portable Network Graphics file (*.png)')

            opencv.imwrite(filename, self.model.processedImage)
