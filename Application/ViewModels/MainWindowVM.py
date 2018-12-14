from Application.Models.MainWindowModel import MainWindowModel
from Application.Views.MainWindowView import MainWindowView
from PyQt5 import QtCore, QtWidgets
import Application.Settings
import cv2 as opencv
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class MainWindowVM(QtCore.QObject):
    loadImageSignal = pyqtSignal(str, bool, name="loadImageSignal")

    def __init__(self, parent=None):
        super().__init__(parent)

        # instantiate the model
        self._model = MainWindowModel()

        # instantiate the QMainWindow object
        self._view = MainWindowView()

        # show the main window
        self._view.show()

        # connect actions signals to slots
        self._view.actionLoadGrayscaleImage.triggered.connect(self._actionLoadGrayscaleImage)
        self._view.actionLoadColorImage.triggered.connect(self._actionLoadColorImage)

    @pyqtSlot()
    def _actionLoadGrayscaleImage(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self._view, caption='Open grayscale file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
                                                            )

        self.loadImageSignal.emit(filePath, True)

    @pyqtSlot()
    def _actionLoadColorImage(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self._view, caption='Open color file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
                                                            )

        self.loadImageSignal.emit(filePath, False)
