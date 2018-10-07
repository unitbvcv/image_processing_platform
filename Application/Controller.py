from Application.Model import Model
from Application.View import MagnifierWindow, MainWindow, PlotterWindow
from pathlib import Path
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2 as opencv
from numpy import *


class Controller(object):
    def __init__(self):
        # instantiate the model
        self.model = Model()

        # instantiate the QMainWindow objects
        self.mainWindow = MainWindow()
        self.plotterWindow = PlotterWindow(self.mainWindow)
        self.magnifierWindow = MagnifierWindow(self.mainWindow)

        # connect the actions to methods
        self.mainWindow.actionExit.triggered.connect(self.actionExit)
        self.mainWindow.actionInvert.triggered.connect(self.actionInvert)
        self.mainWindow.actionLoadColorImage.triggered.connect(self.actionLoadColorImage)
        self.mainWindow.actionLoadGrayscaleImage.triggered.connect(self.actionLoadGrayscaleImage)
        self.mainWindow.actionMagnifier.triggered.connect(self.actionMagnifier)
        self.mainWindow.actionPlotter.triggered.connect(self.actionPlotter)
        self.mainWindow.actionSaveProcessedImage.triggered.connect(self.actionSaveProcessedImage)

        # show the main window
        self.mainWindow.show()

    def actionExit(self):
        QtCore.QCoreApplication.quit()

    def actionInvert(self):
        # TODO
        pass

    def actionLoadColorImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.mainWindow, caption='Open color file',
                                                         filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif'
                                                         )
        if filename != None and Path(filename).is_file():
            self.model.loadOriginalImage(filename, opencv.IMREAD_COLOR)

            self.mainWindow.labelOriginalImage.setPixmap(QtGui.QPixmap.fromImage(
                QtGui.QImage(
                    opencv.cvtColor(self.model.originalImage, opencv.COLOR_BGR2RGB),
                    self.model.originalImage.shape[1],
                    self.model.originalImage.shape[0],
                    QtGui.QImage.Format_RGB888)))
        else:
            self.mainWindow.labelOriginalImage.clear()

        self.model.processedImage = None
        self.mainWindow.labelProcessedImage.clear()

        self.mainWindow.labelOriginalImage.update()
        self.mainWindow.labelProcessedImage.update()

    def actionLoadGrayscaleImage(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.mainWindow, caption='Open color file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif'
                                                            )
        if filename != None and Path(filename).is_file():
            self.model.loadOriginalImage(filename, opencv.IMREAD_GRAYSCALE)

            self.mainWindow.labelOriginalImage.setPixmap(QtGui.QPixmap.fromImage(
                QtGui.QImage(
                    self.model.originalImage,
                    self.model.originalImage.shape[1],
                    self.model.originalImage.shape[0],
                    QtGui.QImage.Format_Grayscale8)))
        else:
            self.mainWindow.labelOriginalImage.clear()

        self.model.processedImage = None
        self.mainWindow.labelProcessedImage.clear()

        self.mainWindow.labelOriginalImage.update()
        self.mainWindow.labelProcessedImage.update()

    def actionMagnifier(self):
        # TODO
        self.magnifierWindow.show()

    def actionPlotter(self):
        # TODO
        self.plotterWindow.show()

    def actionSaveProcessedImage(self):
        # TODO
        pass
