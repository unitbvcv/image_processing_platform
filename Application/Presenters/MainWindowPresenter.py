import os
from collections import deque

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import Signal, Slot

import Application.Settings
import Application.Utils.FileOperations
from Application.Models.MainWindowModel import MainWindowModel
from Application.Views.MainWindowView import MainWindowView
from Application.Utils.Point import Point


class MainWindowPresenter(QtCore.QObject):
    loadOriginalImageSignal = Signal(str, bool, name="loadOriginalImageSignal")
    saveProcessedImageSignal = Signal(str, name="saveProcessedImageSignal")
    openPlotterSignal = Signal(name="openPlotterSignal")
    openMagnifierSignal = Signal(name="openMagnifierSignal")
    saveAsOriginalImageSignal = Signal(name="saveAsOriginalImageSignal")
    mouseMovedImageLabelSignal = Signal(Point, name="mouseMovedImageLabelSignal")
    mousePressedImageLabelSignal = Signal(Point, QtCore.Qt.MouseButton, name="mousePressedImageLabelSignal")
    keyPressedSignal = Signal(QtGui.QKeyEvent, name="keyPressedSignal")
    algorithmTriggered = Signal(str, name="algorithmTriggered")

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

        self._view.keyPressedSignal.connect(self.keyPressedSignal)

    def highlightImageLabelLeftClickPosition(self, clickPosition):
        self._view.labelOriginalImage.setLeftClickPosition(clickPosition)
        self._view.labelProcessedImage.setLeftClickPosition(clickPosition)

    def highlightImageLabelRightClickLastPositions(self, clickPositions: deque):
        self._view.labelOriginalImage.setRightClickLastPositions(clickPositions)
        # self._view.labelProcessedImage.setRightClickLastPositions(clickPositions)

    @Slot(QtGui.QMouseEvent)
    def _onMousePressedImageLabel(self, QMouseEvent):
        if self._view.zoom != 0:
            x = int(QMouseEvent.x() / self._view.zoom)
            y = int(QMouseEvent.y() / self._view.zoom)
            self.mousePressedImageLabelSignal.emit(Point(x, y), QMouseEvent.button())

    @Slot(QtGui.QMouseEvent)
    def _onMouseMovedImageLabel(self, QMouseEvent):
        if self._view.zoom != 0:
            x = int(QMouseEvent.x() / self._view.zoom)
            y = int(QMouseEvent.y() / self._view.zoom)
            self.mouseMovedImageLabelSignal.emit(Point(x, y))

    @Slot(QtCore.QEvent)
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

    @Slot()
    def _actionSaveAsOriginalImage(self):
        self.saveAsOriginalImageSignal.emit()

    @Slot()
    def _actionExit(self):
        QtCore.QCoreApplication.quit()

    @Slot()
    def _actionLoadGrayscaleImage(self):
        fileDialog = QtWidgets.QFileDialog(self._view)
        fileDialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        fileDialog.setNameFilter('Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                 '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)')
        fileDialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        fileDialog.setWindowTitle("Load grayscale image")

        if fileDialog.exec():
            filePath = fileDialog.selectedFiles()[0]

            if Application.Utils.FileOperations.is_path_exists_or_creatable_portable(filePath) and os.path.isfile(filePath):
                self.loadOriginalImageSignal.emit(filePath, True)
            else:
                messagebox = QtWidgets.QMessageBox(self._view)
                messagebox.setWindowTitle("Error")
                messagebox.setText("Load grayscale image: invalid file path.")
                messagebox.setIcon(QtWidgets.QMessageBox.Critical)
                messagebox.exec()

    @Slot()
    def _actionLoadColorImage(self):
        fileDialog = QtWidgets.QFileDialog(self._view)
        fileDialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
        fileDialog.setNameFilter('Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                 '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)')
        fileDialog.setAcceptMode(QtWidgets.QFileDialog.AcceptOpen)
        fileDialog.setWindowTitle("Load color image")

        if fileDialog.exec():
            filePath = fileDialog.selectedFiles()[0]

            if Application.Utils.FileOperations.is_path_exists_or_creatable_portable(filePath) and os.path.isfile(
                    filePath):
                self.loadOriginalImageSignal.emit(filePath, False)
            else:
                messagebox = QtWidgets.QMessageBox(self._view)
                messagebox.setWindowTitle("Error")
                messagebox.setText("Load color image: invalid file path.")
                messagebox.setIcon(QtWidgets.QMessageBox.Critical)
                messagebox.exec()

    @Slot()
    def _actionSaveProcessedImage(self):
        if self._view.labelProcessedImage.isImageSet:
            fileDialog = QtWidgets.QFileDialog(self._view)
            fileDialog.setFileMode(QtWidgets.QFileDialog.AnyFile)
            fileDialog.setNameFilter('Bitmap file (*.bmp *.dib);;'
                                     'JPEG file (*.jpeg *.jpg *.jpe);;'
                                     'JPEG 2000 file (*.jp2);;'
                                     'Portable Network Graphics file (*.png);;'
                                     'WebP file (*.webp);;'
                                     'Sun rasters file (*.ras *.sr);;'
                                     'Tagged Image file (*.tiff *.tif)')
            fileDialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
            fileDialog.setWindowTitle("Save processed image")

            if fileDialog.exec():
                filePath = fileDialog.selectedFiles()[0]

                if Application.Utils.FileOperations.is_path_exists_or_creatable_portable(filePath):
                    self.saveProcessedImageSignal.emit(filePath)
                else:
                    messagebox = QtWidgets.QMessageBox(self._view)
                    messagebox.setWindowTitle("Error")
                    messagebox.setText("Save processed image: invalid file path.")
                    messagebox.setIcon(QtWidgets.QMessageBox.Critical)
                    messagebox.exec()
        else:
            messagebox = QtWidgets.QMessageBox(self._view)
            messagebox.setWindowTitle("Error")
            messagebox.setText("Save processed image: no processed image.")
            messagebox.setIcon(QtWidgets.QMessageBox.Critical)
            messagebox.exec()

    def setOriginalImage(self, image):
        self._view.setOriginalImage(image)

    def setProcessedImage(self, image):
        self._view.setProcessedImage(image)

    def reset(self):
        self._view.setOriginalImage(None)
        self._view.setProcessedImage(None)

        self._view.labelOriginalImage.setLeftClickPosition(None)
        self._view.labelProcessedImage.setLeftClickPosition(None)

        self._view.labelOriginalImage.setRightClickLastPositions(None)
        self._view.labelProcessedImage.setRightClickLastPositions(None)

        self._view.labelOriginalImage.setOverlayData(None)
        self._view.labelProcessedImage.setOverlayData(None)

        self._view.zoomValueResetEvent()

    def registerAlgorithmsInUi(self, algorithms):
        for name, menuPath, before in algorithms:
            newAction = self._view.addMenuAction(name, menuPath, before)
            if newAction is not None:
                newAction.triggered.connect(self._actionAlgorithm)

    @Slot()
    def _actionAlgorithm(self):
        senderAction = self.sender()
        self.algorithmTriggered.emit(senderAction.text())

    def setOriginalImageOverlayData(self, overlayData):
        self._view.labelOriginalImage.setOverlayData(overlayData)

    def setProcessedImageOverlayData(self, overlayData):
        self._view.labelProcessedImage.setOverlayData(overlayData)
