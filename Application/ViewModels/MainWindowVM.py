import os

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import Application.Settings
import Application.Utils.FileOperations
from Application.Models.MainWindowModel import MainWindowModel
from Application.Views.MainWindowView import MainWindowView


class MainWindowVM(QtCore.QObject):
    loadOriginalImageSignal = pyqtSignal(str, bool, name="loadOriginalImageSignal")
    saveProcessedImageSignal = pyqtSignal(str, bool, name="saveProcessedImageSignal")

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
        self._view.actionExit.triggered.connect(self._actionExit)
        self._view.actionSaveProcessedImage.triggered.connect(self._actionSaveProcessedImage)
        
    @pyqtSlot()
    def _actionExit(self):
        QtCore.QCoreApplication.quit()

    @pyqtSlot()
    def _actionLoadGrayscaleImage(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self._view,
            caption='Open grayscale file',
            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
        )

        if Application.Utils.FileOperations.is_path_exists_or_creatable_portable(filePath) and os.path.isfile(filePath):
            self.loadOriginalImageSignal.emit(filePath, True)
        else:
            messagebox = QtWidgets.QMessageBox(self._view)
            messagebox.setText("Load grayscale image: invalid file path.")
            messagebox.exec()

    @pyqtSlot()
    def _actionLoadColorImage(self):
        filePath, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self._view,
            caption='Open color file',
            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
        )

        if Application.Utils.FileOperations.is_path_exists_or_creatable_portable(filePath) and os.path.isfile(filePath):
            self.loadOriginalImageSignal.emit(filePath, False)
        else:
            messagebox = QtWidgets.QMessageBox(self._view)
            messagebox.setText("Load color image: invalid file path.")
            messagebox.exec()

    @pyqtSlot()
    def _actionSaveProcessedImage(self):
        if not self._view.labelProcessedImage.geometry():
            filePath, _ = QtWidgets.QFileDialog.getSaveFileName(
                parent=self._view, 
                caption='Save processed image',
                filter='Bitmap file (*.bmp *.dib);;'
                       'JPEG file (*.jpeg *.jpg *.jpe);;'
                       'JPEG 2000 file (*.jp2);;'
                       'Portable Network Graphics file (*.png);;'
                       'WebP file (*.webp);;'
                       'Sun rasters file (*.ras *.sr);;'
                       'Tagged Image file (*.tiff *.tif)',
                initialFilter='Portable Network Graphics file (*.png)'
            )

            if Application.Utils.FileOperations.is_path_exists_or_creatable_portable(filePath):
                self.saveProcessedImageSignal.emit(filePath)
            else:
                messagebox = QtWidgets.QMessageBox(self._view)
                messagebox.setText("Save processed image: invalid file path.")
                messagebox.exec()
        else:
            messagebox = QtWidgets.QMessageBox(self._view)
            messagebox.setText("Save processed image: no processed image.")
            messagebox.exec()

    def showNewOriginalImage(self, image):
        self._view.labelOriginalImage.setLabelImage(image)
        self._view.labelProcessedImage.setLabelImage(None)

    def reset(self):
        # TODO: clean image labels? and click position? and reset zoom? anything else?
        self._view.labelOriginalImage.setLabelImage(None)
        self._view.labelProcessedImage.setLabelImage(None)
        
        self._view.labelOriginalImage.setClickPosition(None)
        self._view.labelProcessedImage.setClickPosition(None)
