from Application.Models.MainWindowModel import MainWindowModel
from Application.Views.MainWindowView import MainWindowView
from PyQt5 import QtCore, QtWidgets
import Application.Settings
import cv2 as opencv


class MainWindowVM(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        # instantiate the model
        self._model = MainWindowModel()

        # instantiate the QMainWindow object
        self._view = MainWindowView()

        # connect the actions to methods
        self._view.actionExit.triggered.connect(self._actionExit)
        self._view.actionLoadColorImage.triggered.connect(self._actionLoadColorImage)
        self._view.actionLoadGrayscaleImage.triggered.connect(self._actionLoadGrayscaleImage)
        self._view.actionMagnifier.triggered.connect(self._actionMagnifier)
        self._view.actionPlotter.triggered.connect(self._actionPlotter)
        self._view.actionSaveProcessedImage.triggered.connect(self._actionSaveProcessedImage)

        # connect image labels to slots for updating the ui
        # TODO: make some signals in this VM that are emitted by those and sent to the MainVM
        # self._view.labelOriginalImage.mouse_moved.connect(self._mouseMovedEvent)
        # self._view.labelProcessedImage.mouse_moved.connect(self._mouseMovedEvent)
        # self._view.labelOriginalImage.mouse_pressed.connect(self._mousePressedEvent)
        # self._view.labelProcessedImage.mouse_pressed.connect(self._mousePressedEvent)

        # TODO: think about moving those into the view


        # show the main window
        self._view.show()

    def _actionExit(self):
        """
        test
        :return:
        """
        QtCore.QCoreApplication.quit()

    def _actionLoadColorImage(self):
        # TODO: move to MainViewModel

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self.mainWindow, caption='Open color file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
                                                            )

        self._setMagnifierColorModel(Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB)
        self._resetApplicationState()
        self._setImages(originalImage=opencv.imread(filename, opencv.IMREAD_COLOR), processedImage=None)

    def _actionLoadGrayscaleImage(self):
        # TODO: move to MainViewModel, make a signal and emit it

        filename, _ = QtWidgets.QFileDialog.getOpenFileName(parent=self._view, caption='Open grayscale file',
                                                            filter='Image files (*.bmp *.dib *.jpeg *.jpg *.jpe *.jp2 '
                                                                   '*.png *.webp *.pbm *.pgm *.ppm *.ras *.sr *.tiff *.tif)'
                                                            )

        self._setMagnifierColorModel(Application.Settings.MagnifierWindowSettings.ColorSpaces.GRAY)
        self._resetApplicationState()
        self._setImages(originalImage=opencv.imread(filename, opencv.IMREAD_GRAYSCALE), processedImage=None)

    def _actionMagnifier(self):
        # TODO: make a signal and emit it
        self.magnifierWindow.show()

    def _actionPlotter(self):
        # TODO: make a signal and emit it
        self.plotterWindow.show()

    def _actionSaveAsOriginalImage(self):
        # TODO: move to MainViewModel, make a signal and emit it
        self.model.originalImage = self.model.processedImage
        self.model.processedImage = None
        self._setImages(originalImage=self.model.originalImage, processedImage=None)

        if self.model.originalImage is None:
            self._resetApplicationState()

        self._setClickPosition()

    def _actionSaveProcessedImage(self):
        # TODO: move to MainViewModel, make a signal and emit it

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
        # TODO: move most of the code in View, emit a signal that gets catched by MainViewModel and sends the pixel back
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

    def setImages(self, originalImage, processedImage):
        self._view.setImages(processedImage=processedImage, originalImage=originalImage)

        # TODO: ??
        # resetting the images will show them with original resolution
        # they need to be zoomed
        self._zoomValueChangedEvent(self._calculateSliderValueFromZoom(self._zoom))

        self._setClickPosition()
