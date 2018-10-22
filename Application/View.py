from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget
import cv2 as opencv
import Application.Settings
import Application.Utils.ColorSpaceOperations


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._setupUi()
        self._setupImageLabels()

        # synchronize the scrollbars of the scrollAreas
        self.scrollAreaOriginalImage.horizontalScrollBar().valueChanged.connect(
            self.scrollAreaProcessedImage.horizontalScrollBar().setValue)
        self.scrollAreaProcessedImage.horizontalScrollBar().valueChanged.connect(
            self.scrollAreaOriginalImage.horizontalScrollBar().setValue)

        self.scrollAreaOriginalImage.verticalScrollBar().valueChanged.connect(
            self.scrollAreaProcessedImage.verticalScrollBar().setValue)
        self.scrollAreaProcessedImage.verticalScrollBar().valueChanged.connect(
            self.scrollAreaOriginalImage.verticalScrollBar().setValue)

    def _setupUi(self):
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
        self.scrollAreaOriginalImage.setStyleSheet("")
        self.scrollAreaOriginalImage.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollAreaOriginalImage.setWidgetResizable(True)
        self.scrollAreaOriginalImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollAreaOriginalImage.setObjectName("scrollAreaOriginalImage")
        self.scrollAreaWidgetOriginalImage = QtWidgets.QWidget()
        self.scrollAreaWidgetOriginalImage.setGeometry(QtCore.QRect(0, 0, 471, 568))
        self.scrollAreaWidgetOriginalImage.setObjectName("scrollAreaWidgetOriginalImage")
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
        self.horizontalSliderZoom.setMaximum(1)
        self.horizontalSliderZoom.setSingleStep(1)
        self.horizontalSliderZoom.setPageStep(1)
        self.horizontalSliderZoom.setProperty("value", 1)
        self.horizontalSliderZoom.setSliderPosition(1)
        self.horizontalSliderZoom.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderZoom.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSliderZoom.setTickInterval(1)
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

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def _retranslateUi(self):
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

    def _setupImageLabels(self):
        self.stackedLayoutOriginalImage = QtWidgets.QStackedLayout(self.scrollAreaWidgetOriginalImage)
        self.stackedLayoutProcessedImage = QtWidgets.QStackedLayout(self.scrollAreaWidgetProcessedImage)

        self.labelOriginalImage = Application.View.ImageLabel(self.scrollAreaWidgetOriginalImage)
        self.labelOriginalImage.setMouseTracking(True)
        self.labelOriginalImage.setText("")
        self.labelOriginalImage.setScaledContents(False)
        self.labelOriginalImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelOriginalImage.setObjectName("labelOriginalImage")
        self.labelOriginalImage.setGeometry(0, 0, 0, 0)

        self.labelProcessedImage = Application.View.ImageLabel(self.scrollAreaWidgetProcessedImage)
        self.labelProcessedImage.setMouseTracking(True)
        self.labelProcessedImage.setText("")
        self.labelProcessedImage.setScaledContents(False)
        self.labelProcessedImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelProcessedImage.setObjectName("labelProcessedImage")
        self.labelProcessedImage.setGeometry(0, 0, 0, 0)

        self.stackedLayoutOriginalImage.addWidget(self.labelOriginalImage)
        self.stackedLayoutProcessedImage.addWidget(self.labelProcessedImage)

    def setImages(self, originalImage, processedImage):
        self.labelOriginalImage.setLabelImage(originalImage)
        self.labelProcessedImage.setLabelImage(processedImage)


class PlotterWindow(QtWidgets.QMainWindow):
    closing = QtCore.pyqtSignal(QtGui.QCloseEvent, name='closing')
    showing = QtCore.pyqtSignal(QtGui.QShowEvent, name='showing')

    def __init__(self, parent):
        super().__init__(parent)
        self._setupUi()

        self.plotDataItemsOriginalImage = {}
        self.plotDataItemsProcessedImage = {}

    def _setupUi(self):
        self.setObjectName("PlotterWindow")
        self.resize(1000, 500)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.graphicsViewOriginalImage = PlotWidget(self.centralwidget)
        self.graphicsViewOriginalImage.setObjectName("graphicsViewOriginalImage")
        self.horizontalLayout.addWidget(self.graphicsViewOriginalImage)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.labelFunction = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFunction.sizePolicy().hasHeightForWidth())
        self.labelFunction.setSizePolicy(sizePolicy)
        self.labelFunction.setAlignment(QtCore.Qt.AlignCenter)
        self.labelFunction.setObjectName("labelFunction")
        self.verticalLayout_2.addWidget(self.labelFunction)
        self.comboBoxFunction = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxFunction.sizePolicy().hasHeightForWidth())
        self.comboBoxFunction.setSizePolicy(sizePolicy)
        self.comboBoxFunction.setObjectName("comboBoxFunction")
        self.verticalLayout_2.addWidget(self.comboBoxFunction)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.listWidgetVisiblePlots = QtWidgets.QListWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetVisiblePlots.sizePolicy().hasHeightForWidth())
        self.listWidgetVisiblePlots.setSizePolicy(sizePolicy)
        self.listWidgetVisiblePlots.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidgetVisiblePlots.setProperty("showDropIndicator", False)
        self.listWidgetVisiblePlots.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.listWidgetVisiblePlots.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidgetVisiblePlots.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.listWidgetVisiblePlots.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.listWidgetVisiblePlots.setUniformItemSizes(False)
        self.listWidgetVisiblePlots.setObjectName("listWidgetVisiblePlots")
        self.verticalLayout_2.addWidget(self.listWidgetVisiblePlots)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem2)
        self.pushButtonAutoScalePlots = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonAutoScalePlots.sizePolicy().hasHeightForWidth())
        self.pushButtonAutoScalePlots.setSizePolicy(sizePolicy)
        self.pushButtonAutoScalePlots.setObjectName("pushButtonAutoScalePlots")
        self.verticalLayout_2.addWidget(self.pushButtonAutoScalePlots)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.graphicsViewProcessedImage = PlotWidget(self.centralwidget)
        self.graphicsViewProcessedImage.setObjectName("graphicsViewProcessedImage")
        self.horizontalLayout.addWidget(self.graphicsViewProcessedImage)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralwidget)

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def _retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("PlotterWindow", "Plotter"))
        self.labelFunction.setText(_translate("PlotterWindow", "Plot function"))
        self.label.setText(_translate("PlotterWindow", "Visible plots"))
        self.pushButtonAutoScalePlots.setText(_translate("PlotterWindow", "Auto Scale Plots"))

    def reset(self):
        self.graphicsViewOriginalImage.plotItem.clear()
        self.graphicsViewProcessedImage.plotItem.clear()

        for legendString in list(self.plotDataItemsOriginalImage.keys()):
            self.graphicsViewOriginalImage.plotItem.legend.removeItem(legendString)

        for legendString in list(self.plotDataItemsProcessedImage.keys()):
            self.graphicsViewProcessedImage.plotItem.legend.removeItem(legendString)

        self.plotDataItemsOriginalImage.clear()
        self.plotDataItemsProcessedImage.clear()

    def closeEvent(self, QCloseEvent):
        self.closing.emit(QCloseEvent)

    def showEvent(self, QShowEvent):
        self.showing.emit(QShowEvent)

    def autoScalePlots(self):
        plots = list(self.plotDataItemsOriginalImage.values()) + list(self.plotDataItemsProcessedImage.values())
        self.graphicsViewOriginalImage.getPlotItem().getViewBox().autoRange(items=plots)
        self.graphicsViewProcessedImage.getPlotItem().getViewBox().autoRange(items=plots)


class MagnifierWindow(QtWidgets.QMainWindow):
    closing = QtCore.pyqtSignal(QtGui.QCloseEvent, name='closing')
    showing = QtCore.pyqtSignal(QtGui.QShowEvent, name='showing')

    def __init__(self, parent):
        super().__init__(parent)
        self._setupUi()
        self.frameListOriginalImage = []
        self.frameListProcessedImage = []

        # add programmatically a x by x grid of frames
        for row in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
            newRowFrameListOriginalImage = []
            newRowFrameListProcessedImage = []

            for column in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
                newRowFrameListOriginalImage.append(MagnifierPixelFrame())
                self.gridLayoutOriginalImage.addWidget(newRowFrameListOriginalImage[-1], row, column)

                newRowFrameListProcessedImage.append(MagnifierPixelFrame())
                self.gridLayoutProcessedImage.addWidget(newRowFrameListProcessedImage[-1], row, column)

            self.frameListOriginalImage.append(newRowFrameListOriginalImage)
            self.frameListProcessedImage.append(newRowFrameListProcessedImage)

    def _setupUi(self):
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
        self.labelColorModel = QtWidgets.QLabel(self.centralwidget)
        self.labelColorModel.setObjectName("labelColorModel")
        self.horizontalLayoutColorSpace.addWidget(self.labelColorModel)
        self.comboBoxColorModel = QtWidgets.QComboBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxColorModel.sizePolicy().hasHeightForWidth())
        self.comboBoxColorModel.setSizePolicy(sizePolicy)
        self.comboBoxColorModel.setObjectName("comboBoxColorModel")
        self.horizontalLayoutColorSpace.addWidget(self.comboBoxColorModel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutColorSpace.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayoutColorSpace, 0, 0, 1, 2)
        self.setCentralWidget(self.centralwidget)

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def _retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MagnifierWindow", "Magnifier"))
        self.groupBoxOriginalImage.setTitle(_translate("MagnifierWindow", "Original image"))
        self.groupBoxProcessedImage.setTitle(_translate("MagnifierWindow", "Processed image"))
        self.labelColorModel.setText(_translate("MagnifierWindow", "Color model:"))

    def reset(self):
        for row in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
            for column in range(Application.Settings.MagnifierWindowSettings.frameGridSize):
                self.frameListOriginalImage[row][column].setFrameColorGrayLevel(None)
                self.frameListProcessedImage[row][column].setFrameColorGrayLevel(None)

    def closeEvent(self, QCloseEvent):
        self.closing.emit(QCloseEvent)

    def showEvent(self, QShowEvent):
        self.showing.emit(QShowEvent)


class ImageLabel(QtWidgets.QLabel):
    mouse_moved = QtCore.pyqtSignal(QtGui.QMouseEvent, name='mouseMoved')
    mouse_pressed = QtCore.pyqtSignal(QtGui.QMouseEvent, name='mousePressed')
    mouse_leaved = QtCore.pyqtSignal(QtCore.QEvent, name='mouseLeaved')
    finished_painting = QtCore.pyqtSignal(name='finishedPainting')

    def __init__(self, parent=None):
        super().__init__(parent)
        self._qImage = None
        self._zoom = 1.0
        self._clickPosition = None

    def setZoom(self, zoom):
        self._zoom = zoom
        if self._qImage is not None:
            self.setFixedSize(self._qImage.size() * zoom)

    def mouseMoveEvent(self, QMouseEvent):
        self.mouse_moved.emit(QMouseEvent)

    def mousePressEvent(self, QMouseEvent):
        self.mouse_pressed.emit(QMouseEvent)

    def leaveEvent(self, QEvent):
        self.mouse_leaved.emit(QEvent)

    def setClickPosition(self, clickPosition: QtCore.QPoint):
        self._clickPosition = clickPosition
        self.update()

    def setLabelImage(self, image):
        if image is not None:
            if len(image.shape) == 3:
                self._qImage = QtGui.QImage(opencv.cvtColor(image, opencv.COLOR_BGR2RGB).data,
                                             image.shape[1],
                                             image.shape[0],
                                             3 * image.shape[1],
                                             QtGui.QImage.Format_RGB888)
            elif len(image.shape) == 2:
                self._qImage = QtGui.QImage(image.data,
                                             image.shape[1],
                                             image.shape[0],
                                             image.shape[1],
                                             QtGui.QImage.Format_Grayscale8)

            self.setFixedSize(self._qImage.size())
        else:
            self.setFixedSize(0, 0)
            self._qImage = None

        self.update()

    def paintEvent(self, QPaintEvent):
        if self._qImage is not None:
            painter = QtGui.QPainter(self)

            transform = QtGui.QTransform()
            transform.scale(self._zoom, self._zoom)
            painter.setTransform(transform, False)

            painter.drawImage(0, 0, self._qImage)
            painter.setPen(QtGui.QPen(QtCore.Qt.red))
            painter.pen().setWidth(1)

            if self._clickPosition is not None:
                cornerCalcOffset = int(Application.Settings.MagnifierWindowSettings.frameGridSize / 2) + 1

                # vertical line
                painter.drawLine(self._clickPosition.x(), 0, self._clickPosition.x(), (self.height() - 1) // self._zoom )

                # horizontal line
                painter.drawLine(0, self._clickPosition.y(), (self.width() - 1) // self._zoom, self._clickPosition.y())

                # +1 because we need to take into account the thickness of the rectangle itself
                # we want its contents inside to be frameGridSize^2
                painter.drawRect(self._clickPosition.x() - cornerCalcOffset,
                                 self._clickPosition.y() - cornerCalcOffset,
                                 Application.Settings.MagnifierWindowSettings.frameGridSize + 1,
                                 Application.Settings.MagnifierWindowSettings.frameGridSize + 1)


        self.finished_painting.emit()


class MagnifierPixelFrame(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isVisible = False
        self._backgroundColor = QtGui.QColor(255, 255, 255)
        self._colorDisplayFormat = Application.Settings.MagnifierWindowSettings.ColorModels.RGB

    def setColorDisplayFormat(self, format: Application.Settings.MagnifierWindowSettings.ColorModels):
        self._colorDisplayFormat = format
        self.update()

    def setFrameColorRgb(self, red, green, blue):
        if red is not None and green is not None and blue is not None:
            self._backgroundColor = QtGui.QColor(red, green, blue)
            self._isVisible = True
        else:
            self._isVisible = False
            self._backgroundColor = QtGui.QColor(255, 255, 255)

        self.update()

    def setFrameColorGrayLevel(self, grayLevel):
        if grayLevel is not None:
            self._backgroundColor = QtGui.QColor(grayLevel, grayLevel, grayLevel)
            self._isVisible = True
        else:
            self._isVisible = False
            self._backgroundColor = QtGui.QColor(255, 255, 255)

        self.update()

    def paintEvent(self, QPaintEvent):
        if self._isVisible:
            painter = QtGui.QPainter(self)
            painter.fillRect(self.rect(), self._backgroundColor)

            font = QtGui.QFont("Arial")
            font.setPointSize(Application.Settings.MagnifierWindowSettings.fontSize)
            painter.setFont(font)
            fontMetrics = QtGui.QFontMetrics(font)

            if Application.Utils.ColorSpaceOperations.isColorDark(self._backgroundColor):
                painter.setPen(QtCore.Qt.white)
            else:
                painter.setBrush(QtCore.Qt.black)

            if self._colorDisplayFormat is Application.Settings.MagnifierWindowSettings.ColorModels.GRAY:
                text = str((self._backgroundColor.red() + self._backgroundColor.green() +
                            self._backgroundColor.blue()) // 3)

                horizontalAdvance = fontMetrics.horizontalAdvance(text, len(text))

                painter.drawText((self.width() - horizontalAdvance) / 2,
                                 self.height() / 2 + fontMetrics.ascent() / 2,
                                 text)
            elif self._colorDisplayFormat is Application.Settings.MagnifierWindowSettings.ColorModels.CMYK:
                textCyan = str(self._backgroundColor.cyan())
                textMagenta = str(self._backgroundColor.magenta())
                textYellow = str(self._backgroundColor.yellow())
                textBlack = str(self._backgroundColor.black())

                horizontalAdvanceCyan = fontMetrics.horizontalAdvance(textCyan, len(textCyan))
                horizontalAdvanceMagenta = fontMetrics.horizontalAdvance(textMagenta, len(textMagenta))
                horizontalAdvanceYellow = fontMetrics.horizontalAdvance(textYellow, len(textYellow))
                horizontalAdvanceBlack = fontMetrics.horizontalAdvance(textBlack, len(textBlack))

                # the frame is split into equal rectangles called zones
                # this tries to center the text in one of the 3 zones of the frame
                # the (usually) visible part of the text is the ascent, not the height
                # fonts usually have a baseline; the font will have parts of it below the baseline
                # but those are exceptions (eg. Q - the line below the O that forms the Q is below the baseline)
                zoneHeight = (self.height() - Application.Settings.MagnifierWindowSettings.fourZoneHeightPadding) / 4
                halfFontAscent = fontMetrics.ascent() / 2
                halfZoneHeight = zoneHeight / 2
                zoneHeightOffset = halfZoneHeight - halfFontAscent - Application.Settings.MagnifierWindowSettings.fourZoneHeightPadding / 2

                painter.drawText((self.width() - horizontalAdvanceCyan) / 2, zoneHeight - zoneHeightOffset,
                                 textCyan)
                painter.drawText((self.width() - horizontalAdvanceMagenta) / 2, zoneHeight * 2 - zoneHeightOffset,
                                 textMagenta)
                painter.drawText((self.width() - horizontalAdvanceYellow) / 2, zoneHeight * 3 - zoneHeightOffset,
                                 textYellow)
                painter.drawText((self.width() - horizontalAdvanceBlack) / 2, zoneHeight * 4 - zoneHeightOffset,
                                 textBlack)
            else:
                if self._colorDisplayFormat is Application.Settings.MagnifierWindowSettings.ColorModels.RGB:
                    textFirst = str(self._backgroundColor.red())
                    textSecond = str(self._backgroundColor.green())
                    textThird = str(self._backgroundColor.blue())
                elif self._colorDisplayFormat is Application.Settings.MagnifierWindowSettings.ColorModels.HSL:
                    textFirst = str(self._backgroundColor.hue())
                    textSecond = str(self._backgroundColor.saturation())
                    textThird = str(self._backgroundColor.lightness())
                elif self._colorDisplayFormat is Application.Settings.MagnifierWindowSettings.ColorModels.HSV:
                    textFirst = str(self._backgroundColor.hue())
                    textSecond = str(self._backgroundColor.saturation())
                    textThird = str(self._backgroundColor.value())

                horizontalAdvanceRed = fontMetrics.horizontalAdvance(textFirst, len(textFirst))
                horizontalAdvanceGreen = fontMetrics.horizontalAdvance(textSecond, len(textSecond))
                horizontalAdvanceBlue = fontMetrics.horizontalAdvance(textThird, len(textThird))

                # the frame is split into equal rectangles called zones
                # this tries to center the text in one of the 3 zones of the frame
                # the (usually) visible part of the text is the ascent, not the height
                # fonts usually have a baseline; the font will have parts of it below the baseline
                # but those are exceptions (eg. Q - the line below the O that forms the Q is below the baseline)
                zoneHeight = (self.height() - Application.Settings.MagnifierWindowSettings.threeZoneHeightPadding) / 3
                halfFontAscent = fontMetrics.ascent() / 2
                halfZoneHeight = zoneHeight / 2
                zoneHeightOffset = halfZoneHeight - halfFontAscent - Application.Settings.MagnifierWindowSettings.threeZoneHeightPadding / 2

                painter.drawText((self.width() - horizontalAdvanceRed) / 2, zoneHeight - zoneHeightOffset,
                                 textFirst)
                painter.drawText((self.width() - horizontalAdvanceGreen) / 2, zoneHeight * 2 - zoneHeightOffset,
                                 textSecond)
                painter.drawText((self.width() - horizontalAdvanceBlue) / 2, zoneHeight * 3 - zoneHeightOffset,
                                 textThird)
