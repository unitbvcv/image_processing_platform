from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import cv2 as opencv
import numpy
import Application.Settings


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.__setupUi()

        # synchronize the scrollbars of the scrollAreas
        self.scrollAreaOriginalImage.horizontalScrollBar().valueChanged.connect(
            self.scrollAreaProcessedImage.horizontalScrollBar().setValue)
        self.scrollAreaProcessedImage.horizontalScrollBar().valueChanged.connect(
            self.scrollAreaOriginalImage.horizontalScrollBar().setValue)

        self.scrollAreaOriginalImage.verticalScrollBar().valueChanged.connect(
            self.scrollAreaProcessedImage.verticalScrollBar().setValue)
        self.scrollAreaProcessedImage.verticalScrollBar().valueChanged.connect(
            self.scrollAreaOriginalImage.verticalScrollBar().setValue)

    def __setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1024, 768)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayoutImages = QtWidgets.QHBoxLayout()
        self.horizontalLayoutImages.setSpacing(6)
        self.horizontalLayoutImages.setObjectName("horizontalLayoutImages")
        self.groupBoxOriginalImage = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxOriginalImage.sizePolicy().hasHeightForWidth())
        self.groupBoxOriginalImage.setSizePolicy(sizePolicy)
        self.groupBoxOriginalImage.setObjectName("groupBoxOriginalImage")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBoxOriginalImage)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollAreaOriginalImage = QtWidgets.QScrollArea(self.groupBoxOriginalImage)
        self.scrollAreaOriginalImage.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollAreaOriginalImage.setWidgetResizable(True)
        self.scrollAreaOriginalImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollAreaOriginalImage.setObjectName("scrollAreaOriginalImage")
        self.scrollAreaWidgetOriginalImage = QtWidgets.QWidget()
        self.scrollAreaWidgetOriginalImage.setGeometry(QtCore.QRect(0, 0, 471, 568))
        self.scrollAreaWidgetOriginalImage.setObjectName("scrollAreaWidgetOriginalImage")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetOriginalImage)
        self.horizontalLayout_3.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.labelOriginalImage = Label(self.scrollAreaWidgetOriginalImage)
        self.labelOriginalImage.setMouseTracking(True)
        self.labelOriginalImage.setText("")
        self.labelOriginalImage.setScaledContents(False)
        self.labelOriginalImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelOriginalImage.setObjectName("labelOriginalImage")
        self.horizontalLayout_3.addWidget(self.labelOriginalImage)
        self.scrollAreaOriginalImage.setWidget(self.scrollAreaWidgetOriginalImage)
        self.horizontalLayout.addWidget(self.scrollAreaOriginalImage)
        self.horizontalLayoutImages.addWidget(self.groupBoxOriginalImage)
        self.groupBoxProcessedImage = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxProcessedImage.sizePolicy().hasHeightForWidth())
        self.groupBoxProcessedImage.setSizePolicy(sizePolicy)
        self.groupBoxProcessedImage.setObjectName("groupBoxProcessedImage")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBoxProcessedImage)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollAreaProcessedImage = QtWidgets.QScrollArea(self.groupBoxProcessedImage)
        self.scrollAreaProcessedImage.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollAreaProcessedImage.setWidgetResizable(True)
        self.scrollAreaProcessedImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollAreaProcessedImage.setObjectName("scrollAreaProcessedImage")
        self.scrollAreaWidgetProcessedImage = QtWidgets.QWidget()
        self.scrollAreaWidgetProcessedImage.setGeometry(QtCore.QRect(0, 0, 470, 568))
        self.scrollAreaWidgetProcessedImage.setObjectName("scrollAreaWidgetProcessedImage")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.scrollAreaWidgetProcessedImage)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.labelProcessedImage = Label(self.scrollAreaWidgetProcessedImage)
        self.labelProcessedImage.setMouseTracking(True)
        self.labelProcessedImage.setText("")
        self.labelProcessedImage.setScaledContents(False)
        self.labelProcessedImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelProcessedImage.setObjectName("labelProcessedImage")
        self.horizontalLayout_4.addWidget(self.labelProcessedImage)
        self.scrollAreaProcessedImage.setWidget(self.scrollAreaWidgetProcessedImage)
        self.horizontalLayout_2.addWidget(self.scrollAreaProcessedImage)
        self.horizontalLayoutImages.addWidget(self.groupBoxProcessedImage)
        self.verticalLayout.addLayout(self.horizontalLayoutImages)
        self.horizontalLayoutZoom = QtWidgets.QHBoxLayout()
        self.horizontalLayoutZoom.setSpacing(6)
        self.horizontalLayoutZoom.setObjectName("horizontalLayoutZoom")
        self.buttonResetZoom = QtWidgets.QPushButton(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonResetZoom.sizePolicy().hasHeightForWidth())
        self.buttonResetZoom.setSizePolicy(sizePolicy)
        self.buttonResetZoom.setMinimumSize(QtCore.QSize(0, 33))
        self.buttonResetZoom.setObjectName("buttonResetZoom")
        self.horizontalLayoutZoom.addWidget(self.buttonResetZoom)
        self.horizontalSliderZoom = QtWidgets.QSlider(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSliderZoom.sizePolicy().hasHeightForWidth())
        self.horizontalSliderZoom.setSizePolicy(sizePolicy)
        self.horizontalSliderZoom.setMinimumSize(QtCore.QSize(0, 33))
        self.horizontalSliderZoom.setMaximum(198)
        self.horizontalSliderZoom.setSliderPosition(18)
        self.horizontalSliderZoom.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderZoom.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSliderZoom.setTickInterval(2)
        self.horizontalSliderZoom.setObjectName("horizontalSliderZoom")
        self.horizontalLayoutZoom.addWidget(self.horizontalSliderZoom)
        self.labelZoomFactor = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelZoomFactor.sizePolicy().hasHeightForWidth())
        self.labelZoomFactor.setSizePolicy(sizePolicy)
        self.labelZoomFactor.setMinimumSize(QtCore.QSize(0, 33))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labelZoomFactor.setFont(font)
        self.labelZoomFactor.setObjectName("labelZoomFactor")
        self.horizontalLayoutZoom.addWidget(self.labelZoomFactor)
        self.verticalLayout.addLayout(self.horizontalLayoutZoom)
        self.gridLayoutMouseLabels = QtWidgets.QGridLayout()
        self.gridLayoutMouseLabels.setSpacing(6)
        self.gridLayoutMouseLabels.setObjectName("gridLayoutMouseLabels")
        self.labelOriginalImagePixelValue = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelOriginalImagePixelValue.sizePolicy().hasHeightForWidth())
        self.labelOriginalImagePixelValue.setSizePolicy(sizePolicy)
        self.labelOriginalImagePixelValue.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelOriginalImagePixelValue.setFont(font)
        self.labelOriginalImagePixelValue.setText("")
        self.labelOriginalImagePixelValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOriginalImagePixelValue.setObjectName("labelOriginalImagePixelValue")
        self.gridLayoutMouseLabels.addWidget(self.labelOriginalImagePixelValue, 0, 0, 1, 1)
        self.labelProcessedImagePixelValue = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelProcessedImagePixelValue.sizePolicy().hasHeightForWidth())
        self.labelProcessedImagePixelValue.setSizePolicy(sizePolicy)
        self.labelProcessedImagePixelValue.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelProcessedImagePixelValue.setFont(font)
        self.labelProcessedImagePixelValue.setText("")
        self.labelProcessedImagePixelValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelProcessedImagePixelValue.setObjectName("labelProcessedImagePixelValue")
        self.gridLayoutMouseLabels.addWidget(self.labelProcessedImagePixelValue, 0, 1, 1, 1)
        self.labelMousePosition = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMousePosition.sizePolicy().hasHeightForWidth())
        self.labelMousePosition.setSizePolicy(sizePolicy)
        self.labelMousePosition.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelMousePosition.setFont(font)
        self.labelMousePosition.setText("")
        self.labelMousePosition.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMousePosition.setObjectName("labelMousePosition")
        self.gridLayoutMouseLabels.addWidget(self.labelMousePosition, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayoutMouseLabels)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        self.setMenuBar(self.menuBar)
        self.actionLoadGrayscaleImage = QtWidgets.QAction(self)
        self.actionLoadGrayscaleImage.setObjectName("actionLoadGrayscaleImage")
        self.actionLoadColorImage = QtWidgets.QAction(self)
        self.actionLoadColorImage.setObjectName("actionLoadColorImage")
        self.actionSaveProcessedImage = QtWidgets.QAction(self)
        self.actionSaveProcessedImage.setObjectName("actionSaveProcessedImage")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.actionMagnifier = QtWidgets.QAction(self)
        self.actionMagnifier.setObjectName("actionMagnifier")
        self.actionPlotter = QtWidgets.QAction(self)
        self.actionPlotter.setObjectName("actionPlotter")
        self.actionInvert = QtWidgets.QAction(self)
        self.actionInvert.setObjectName("actionInvert")
        self.menuFile.addAction(self.actionLoadGrayscaleImage)
        self.menuFile.addAction(self.actionLoadColorImage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveProcessedImage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuTools.addAction(self.actionMagnifier)
        self.menuTools.addAction(self.actionPlotter)
        self.menuTools.addSeparator()
        self.menuTools.addAction(self.actionInvert)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())

        self.__retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Image Processing Tool"))
        self.groupBoxOriginalImage.setTitle(_translate("MainWindow", "Original image"))
        self.groupBoxProcessedImage.setTitle(_translate("MainWindow", "Processed image"))
        self.buttonResetZoom.setText(_translate("MainWindow", "Reset"))
        self.labelZoomFactor.setText(_translate("MainWindow", "1.00x"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionLoadGrayscaleImage.setText(_translate("MainWindow", "Load grayscale image"))
        self.actionLoadColorImage.setText(_translate("MainWindow", "Load color image"))
        self.actionSaveProcessedImage.setText(_translate("MainWindow", "Save processed image"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionMagnifier.setText(_translate("MainWindow", "Magnifier"))
        self.actionPlotter.setText(_translate("MainWindow", "Plotter"))
        self.actionInvert.setText(_translate("MainWindow", "Invert"))

    def setImages(self, originalImage, processedImage):
        self.labelOriginalImage.setLabelImage(originalImage)
        self.labelProcessedImage.setLabelImage(processedImage)


class PlotterWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.__setupUi()

        self.plotLegendStringList = []

    def __setupUi(self):
        self.setObjectName("PlotterWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.labelFunction = QtWidgets.QLabel(self.centralwidget)
        self.labelFunction.setObjectName("labelFunction")
        self.horizontalLayout_2.addWidget(self.labelFunction)
        self.comboBoxFunction = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxFunction.sizePolicy().hasHeightForWidth())
        self.comboBoxFunction.setSizePolicy(sizePolicy)
        self.comboBoxFunction.setObjectName("comboBoxFunction")
        self.horizontalLayout_2.addWidget(self.comboBoxFunction)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsViewOriginalImage = PlotWidget(self.centralwidget)
        self.graphicsViewOriginalImage.setObjectName("graphicsViewOriginalImage")
        self.horizontalLayout.addWidget(self.graphicsViewOriginalImage)
        self.graphicsViewProcessedImage = PlotWidget(self.centralwidget)
        self.graphicsViewProcessedImage.setObjectName("graphicsViewProcessedImage")
        self.horizontalLayout.addWidget(self.graphicsViewProcessedImage)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralwidget)

        self.__retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("PlotterWindow", "Plotter"))
        self.labelFunction.setText(_translate("PlotterWindow", "Plot function:"))

    def reset(self):
        self.graphicsViewOriginalImage.plotItem.clear()
        self.graphicsViewProcessedImage.plotItem.clear()

        for legendString in self.plotLegendStringList:
            self.graphicsViewOriginalImage.plotItem.legend.removeItem(legendString)
            self.graphicsViewProcessedImage.plotItem.legend.removeItem(legendString)

        self.plotLegendStringList.clear()


class MagnifierWindow(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__(parent)
        self.__setupUi()
        self.frameListOriginalImage = []
        self.frameListProcessedImage = []

        # add programmatically a x by x grid of frames
        for row in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
            newRowFrameListOriginalImage = []
            newRowFrameListProcessedImage = []

            for column in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
                newRowFrameListOriginalImage.append(Frame())
                self.gridLayoutOriginalImage.addWidget(newRowFrameListOriginalImage[-1], row, column)

                newRowFrameListProcessedImage.append(Frame())
                self.gridLayoutProcessedImage.addWidget(newRowFrameListProcessedImage[-1], row, column)

            self.frameListOriginalImage.append(newRowFrameListOriginalImage)
            self.frameListProcessedImage.append(newRowFrameListProcessedImage)

    def __setupUi(self):
        self.setObjectName("MagnifierWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBoxOriginalImage = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxOriginalImage.sizePolicy().hasHeightForWidth())
        self.groupBoxOriginalImage.setSizePolicy(sizePolicy)
        self.groupBoxOriginalImage.setObjectName("groupBoxOriginalImage")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxOriginalImage)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayoutOriginalImage = QtWidgets.QGridLayout()
        self.gridLayoutOriginalImage.setSpacing(2)
        self.gridLayoutOriginalImage.setObjectName("gridLayoutOriginalImage")
        self.gridLayout_3.addLayout(self.gridLayoutOriginalImage, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBoxOriginalImage, 1, 0, 1, 1)
        self.groupBoxProcessedImage = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxProcessedImage.sizePolicy().hasHeightForWidth())
        self.groupBoxProcessedImage.setSizePolicy(sizePolicy)
        self.groupBoxProcessedImage.setObjectName("groupBoxProcessedImage")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBoxProcessedImage)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayoutProcessedImage = QtWidgets.QGridLayout()
        self.gridLayoutProcessedImage.setSpacing(2)
        self.gridLayoutProcessedImage.setObjectName("gridLayoutProcessedImage")
        self.gridLayout_4.addLayout(self.gridLayoutProcessedImage, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBoxProcessedImage, 1, 1, 1, 1)
        self.horizontalLayoutColorSpace = QtWidgets.QHBoxLayout()
        self.horizontalLayoutColorSpace.setObjectName("horizontalLayoutColorSpace")
        self.labelColorSpace = QtWidgets.QLabel(self.centralwidget)
        self.labelColorSpace.setObjectName("labelColorSpace")
        self.horizontalLayoutColorSpace.addWidget(self.labelColorSpace)
        self.comboBoxColorSpace = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxColorSpace.sizePolicy().hasHeightForWidth())
        self.comboBoxColorSpace.setSizePolicy(sizePolicy)
        self.comboBoxColorSpace.setObjectName("comboBoxColorSpace")
        self.horizontalLayoutColorSpace.addWidget(self.comboBoxColorSpace)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutColorSpace.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayoutColorSpace, 0, 0, 1, 2)
        self.setCentralWidget(self.centralwidget)

        self.__retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MagnifierWindow", "Magnifier"))
        self.groupBoxOriginalImage.setTitle(_translate("MagnifierWindow", "Original image"))
        self.groupBoxProcessedImage.setTitle(_translate("MagnifierWindow", "Processed image"))
        self.labelColorSpace.setText(_translate("MagnifierWindow", "Color space:"))

    def reset(self):
        for row in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
            for column in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
                self.frameListOriginalImage[row][column].setFrameColorGrayLevel(None)
                self.frameListProcessedImage[row][column].setFrameColorGrayLevel(None)


class Label(QtWidgets.QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__clickPosition = None
        self.__image = None

    mouse_moved = QtCore.pyqtSignal(QtGui.QMouseEvent, name='mouseMoved')
    mouse_pressed = QtCore.pyqtSignal(QtGui.QMouseEvent, name='mousePressed')

    def setClickPosition(self, clickPosition : QtCore.QPoint):
        self.__clickPosition = clickPosition
        self.update()

    def setLabelImage(self, image):
        self.__image = image
        if image is not None:
            self.setFixedSize(image.shape[1], image.shape[0])
        else:
            self.setFixedSize(0, 0)
        self.update()

    def mouseMoveEvent(self, QMouseEvent):
        self.mouse_moved.emit(QMouseEvent)

    def mousePressEvent(self, QMouseEvent):
        self.mouse_pressed.emit(QMouseEvent)

    def paintEvent(self, QPaintEvent):
        painter = QtGui.QPainter(self)

        if self.__image is not None:
            if len(self.__image.shape) == 3:
                painter.drawImage(0, 0, QtGui.QImage(opencv.cvtColor(self.__image, opencv.COLOR_BGR2RGB).data,
                                                     self.__image.shape[1],
                                                     self.__image.shape[0],
                                                     3 * self.__image.shape[1],
                                                     QtGui.QImage.Format_RGB888))
            elif len(self.__image.shape) == 2:
                painter.drawImage(0, 0, QtGui.QImage(self.__image.data,
                                                     self.__image.shape[1],
                                                     self.__image.shape[0],
                                                     self.__image.shape[1],
                                                     QtGui.QImage.Format_Grayscale8))

        if self.__clickPosition is not None:
            cornerCalcOffset = Application.Settings.MagnifierWindowSettings.frameGridSize // 2

            painter.drawLine(self.__clickPosition.x(), 0, self.__clickPosition.x(), self.height() - 1)
            painter.drawLine(0, self.__clickPosition.y(), self.width() - 1, self.__clickPosition.y())
            painter.drawRect(self.__clickPosition.x() - cornerCalcOffset,
                             self.__clickPosition.y() - cornerCalcOffset,
                             Application.Settings.MagnifierWindowSettings.frameGridSize,
                             Application.Settings.MagnifierWindowSettings.frameGridSize)


class Frame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__isVisible = False
        self.__backgroundColor = QtGui.QColor(255, 255, 255)
        self.__colorDisplayFormat = Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB

    def setColorDisplayFormat(self, format : Application.Settings.MagnifierWindowSettings.ColorSpaces):
        self.__colorDisplayFormat = format
        self.update()

    def setFrameColorRgb(self, red, green, blue):
        if red is not None and green is not None and blue is not None:
            self.__backgroundColor = QtGui.QColor(red, green, blue)
            self.__isVisible = True
        else:
            self.__isVisible = False
            self.__backgroundColor = QtGui.QColor(255, 255, 255)

        self.update()

    def setFrameColorGrayLevel(self, grayLevel):
        if grayLevel is not None:
            self.__backgroundColor = QtGui.QColor(grayLevel, grayLevel, grayLevel)
            self.__isVisible = True
        else:
            self.__isVisible = False
            self.__backgroundColor = QtGui.QColor(255, 255, 255)

        self.update()

    def paintEvent(self, QPaintEvent):
        if self.__isVisible:
            painter = QtGui.QPainter(self)
            painter.fillRect(self.rect(), self.__backgroundColor)

            font = QtGui.QFont("Arial")
            font.setPointSize(8)
            painter.setFont(font)
            fontMetrics = QtGui.QFontMetrics(font)

            if self.__backgroundColor.lightness() < 127:
                painter.setPen(QtCore.Qt.white)
            else:
                painter.setBrush(QtCore.Qt.black)

            if self.__colorDisplayFormat is Application.Settings.MagnifierWindowSettings.ColorSpaces.GRAY:
                text = str((self.__backgroundColor.red() + self.__backgroundColor.green() + self.__backgroundColor.blue()) // 3)

                horizontalAdvance = fontMetrics.horizontalAdvance(text, len(text))

                painter.drawText((self.width() - horizontalAdvance) / 2,
                                 self.height() / 2 + fontMetrics.height() / 2,
                                 text)
            elif self.__colorDisplayFormat is Application.Settings.MagnifierWindowSettings.ColorSpaces.CMYK:
                # TODO: proper text positions
                textCyan = str(self.__backgroundColor.cyan())
                textMagenta = str(self.__backgroundColor.magenta())
                textYellow = str(self.__backgroundColor.yellow())
                textBlack = str(self.__backgroundColor.black())

                horizontalAdvanceCyan = fontMetrics.horizontalAdvance(textCyan, len(textCyan))
                horizontalAdvanceMagenta = fontMetrics.horizontalAdvance(textMagenta, len(textMagenta))
                horizontalAdvanceYellow = fontMetrics.horizontalAdvance(textYellow, len(textYellow))
                horizontalAdvanceBlack = fontMetrics.horizontalAdvance(textBlack, len(textBlack))

                textZoneHeight = (self.height() - 5) / 4

                painter.drawText((self.width() - horizontalAdvanceCyan) / 2, textZoneHeight, textCyan)
                painter.drawText((self.width() - horizontalAdvanceMagenta) / 2, textZoneHeight * 2, textMagenta)
                painter.drawText((self.width() - horizontalAdvanceYellow) / 2, textZoneHeight * 3, textYellow)
                painter.drawText((self.width() - horizontalAdvanceBlack) / 2, textZoneHeight * 4, textBlack)
            else:
                if self.__colorDisplayFormat is Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB:
                    textFirst = str(self.__backgroundColor.red())
                    textSecond = str(self.__backgroundColor.green())
                    textThird = str(self.__backgroundColor.blue())
                elif self.__colorDisplayFormat is Application.Settings.MagnifierWindowSettings.ColorSpaces.HSL:
                    textFirst = str(self.__backgroundColor.hue())
                    textSecond = str(self.__backgroundColor.saturation())
                    textThird = str(self.__backgroundColor.lightness())
                elif self.__colorDisplayFormat is Application.Settings.MagnifierWindowSettings.ColorSpaces.HSV:
                    textFirst = str(self.__backgroundColor.hue())
                    textSecond = str(self.__backgroundColor.saturation())
                    textThird = str(self.__backgroundColor.value())

                horizontalAdvanceRed = fontMetrics.horizontalAdvance(textFirst, len(textFirst))
                horizontalAdvanceGreen = fontMetrics.horizontalAdvance(textSecond, len(textSecond))
                horizontalAdvanceBlue = fontMetrics.horizontalAdvance(textThird, len(textThird))

                middleTextLine = self.height() / 2 + fontMetrics.height() / 3

                painter.drawText((self.width() - horizontalAdvanceRed) / 2, middleTextLine - fontMetrics.height(), textFirst)
                painter.drawText((self.width() - horizontalAdvanceGreen) / 2, middleTextLine, textSecond)
                painter.drawText((self.width() - horizontalAdvanceBlue) / 2, middleTextLine + fontMetrics.height(), textThird)
