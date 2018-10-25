from PyQt5 import QtCore, QtGui, QtWidgets
from Application.Views import MagnifierPixelFrame
import Application.Settings


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