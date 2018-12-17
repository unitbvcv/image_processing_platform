import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal, pyqtSlot

import Application.Settings
import Application.Utils.FileOperations
from Application.Models.MainWindowModel import MainWindowModel
from Application.Views.MainWindowView import MainWindowView


class MainWindowVM(QtCore.QObject):
    loadOriginalImageSignal = pyqtSignal(str, bool, name="loadOriginalImageSignal")
    saveProcessedImageSignal = pyqtSignal(str, name="saveProcessedImageSignal")
    openPlotterSignal = pyqtSignal(name="openPlotterSignal")
    openMagnifierSignal = pyqtSignal(name="openMagnifierSignal")
    saveAsOriginalImageSignal = pyqtSignal(name="saveAsOriginalImageSignal")
    mouseMovedImageLabelSignal = pyqtSignal(QtCore.QPoint, name="mouseMovedImageLabelSignal")
    mousePressedImageLabelSignal = pyqtSignal(QtCore.QPoint, name="mousePressedImageLabelSignal")

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
        self._view.actionPlotter.triggered.connect(self.openPlotterSignal)
        self._view.actionMagnifier.triggered.connect(self.openMagnifierSignal)
        self._view.actionSaveAsOriginalImage.triggered.connect(self._actionSaveAsOriginalImage)

        # connect image labels signals to slots
        self._view.labelOriginalImage.mouseMovedSignal.connect(self._onMouseMovedImageLabel)
        self._view.labelProcessedImage.mouseMovedSignal.connect(self._onMouseMovedImageLabel)
        self._view.labelOriginalImage.mouseLeavedSignal.connect(self._onMouseLeavedImageLabel)
        self._view.labelProcessedImage.mouseLeavedSignal.connect(self._onMouseLeavedImageLabel)
        self._view.labelOriginalImage.mousePressedSignal.connect(self._onMousePressedImageLabel)
        self._view.labelProcessedImage.mousePressedSignal.connect(self._onMousePressedImageLabel)

    def highlightImageLabelClickPosition(self, clickPosition):
        if self._view.labelOriginalImage.isImageSet:
            self._view.labelOriginalImage.setClickPosition(clickPosition)
        if self._view.labelProcessedImage.isImageSet:
            self._view.labelProcessedImage.setClickPosition(clickPosition)

    @pyqtSlot(QtGui.QMouseEvent)
    def _onMousePressedImageLabel(self, QMouseEvent):
        if self._view.zoom != 0:
            x = int(QMouseEvent.x() / self._view.zoom)
            y = int(QMouseEvent.y() / self._view.zoom)
            self.mousePressedImageLabelSignal.emit(QtCore.QPoint(x, y))

    @pyqtSlot(QtGui.QMouseEvent)
    def _onMouseMovedImageLabel(self, QMouseEvent):
        if self._view.zoom != 0:
            x = int(QMouseEvent.x() / self._view.zoom)
            y = int(QMouseEvent.y() / self._view.zoom)
            self.mouseMovedImageLabelSignal.emit(QtCore.QPoint(x, y))

    @pyqtSlot(QtCore.QEvent)
    def _onMouseLeavedImageLabel(self, QEvent):
        self._view.labelMousePosition.setText('')
        self._view.labelOriginalImagePixelValue.setText('')
        self._view.labelProcessedImagePixelValue.setText('')

    def setMousePositionLabelText(self, text):
        self._view.labelMousePosition.setText(text)

    def setOriginalImagePixelValueLabelText(self, text):
        self._view.labelOriginalImagePixelValue.setText(text)

    def setProcessedImagePixelValueLabelText(self, text):
        self._view.labelProcessedImagePixelValue.setText(text)

    @pyqtSlot()
    def _actionSaveAsOriginalImage(self):
        self.saveAsOriginalImageSignal.emit()
        
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
        if self._view.labelProcessedImage.isImageSet:
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
