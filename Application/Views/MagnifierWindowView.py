import numpy as np

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSignal

from Application.Settings import MagnifierWindowSettings
from Application.Views.MagnifierPixelFrame import MagnifierPixelFrame


class MagnifierWindowView(QtWidgets.QMainWindow):
    """
    TODO: MagnifierWindow documentation
    """

    closing = pyqtSignal(QtGui.QCloseEvent, name='closing')

    def __init__(self, parent=None):
        """
        TODO: document MagnifierWindow constructor
        :param parent:
        """
        super().__init__(parent)
        self._setupUi()

        rows = MagnifierWindowSettings.frameGridSize
        columns = MagnifierWindowSettings.frameGridSize
        generateList = lambda nbRows, nbColumns: [
            [MagnifierPixelFrame() for column in range(nbColumns)] for row in range(nbRows)
        ]
        self.frameListOriginalImage = generateList(rows, columns)
        self.frameListProcessedImage = generateList(rows, columns)  # can't use copy/deepcopy

        # add programmatically a rows by columns grid of frames
        for row in range(rows):
            for column in range(columns):
                self.gridLayoutOriginalImage.addWidget(self.frameListOriginalImage[row][column], row, column)
                self.gridLayoutProcessedImage.addWidget(self.frameListProcessedImage[row][column], row, column)

    def _setupUi(self):
        """
        TODO: document MagnifierWindow _setupUi
        """
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
        self.comboBoxColorSpace.addItems(
            [item.value[1] for item in MagnifierWindowSettings.ColorSpaces])
        self.comboBoxColorSpace.setObjectName("comboBoxColorSpace")
        self.horizontalLayoutColorSpace.addWidget(self.comboBoxColorSpace)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayoutColorSpace.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayoutColorSpace, 0, 0, 1, 2)
        self.setCentralWidget(self.centralwidget)

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def _retranslateUi(self):
        """
        TODO: document MagnifierWindow _retranslateUi
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MagnifierWindow", "Magnifier"))
        self.groupBoxOriginalImage.setTitle(_translate("MagnifierWindow", "Original image"))
        self.groupBoxProcessedImage.setTitle(_translate("MagnifierWindow", "Processed image"))
        self.labelColorSpace.setText(_translate("MagnifierWindow", "Color space:"))

    def setColorSpace(self, colorSpace : MagnifierWindowSettings.ColorSpaces):
        """
        TODO: document MagnifierWindow setColorSpace
        :return:
        """
        for row in range(MagnifierWindowSettings.frameGridSize):
            for column in range(MagnifierWindowSettings.frameGridSize):
                self.frameListOriginalImage[row][column].setColorDisplayFormat(colorSpace)
                self.frameListProcessedImage[row][column].setColorDisplayFormat(colorSpace)

    def setOriginalPixelFrameColor(self, row, column, color):
        """
        TODO: document MagnifierWindow setOriginalPixelFrameColor
        :return:
        """
        pixelFrame = self.frameListOriginalImage[row][column]
        self._setPixelFrameColor(pixelFrame, color)

    def setProcessedPixelFrameColor(self, row, column, color):
        """
        TODO: document MagnifierWindow setProcessedPixelFrameColor
        :return:
        """
        pixelFrame = self.frameListProcessedImage[row][column]
        self._setPixelFrameColor(pixelFrame, color)

    def _setPixelFrameColor(self, pixelFrame, color):
        """
        TODO: document MagnifierWindow _setPixelFrameColor
        :return:
        """
        if isinstance(color, int):
            pixelFrame.setFrameColorGrayLevel(color)
        elif isinstance(color, np.ndarray):
            pixelFrame.setFrameColorRgb(red=color[0], green=color[1], blue=color[2])
        else:
            pixelFrame.setFrameColorGrayLevel(None)

    def reset(self):
        """
        Clears the settings of every pixel frame (not the color space) and then sets the color space from the combo box.
        Updating the combo box may or may not call the slot in the VM (depending on whether RGB was already set or not).
        If it calls the slot, every pixel frame will redraw itself when the color space is set.
        If it doesn't call the slot, an update must be called from the window.
        TODO: document MagnifierWindow reset
        :return: None
        """
        for row in range(MagnifierWindowSettings.frameGridSize):
            for column in range(MagnifierWindowSettings.frameGridSize):
                self.frameListOriginalImage[row][column].clear()
                self.frameListProcessedImage[row][column].clear()
        self.comboBoxColorSpace.setCurrentIndex(0)
        self.update()

    def closeEvent(self, QCloseEvent):
        """
        TODO: document MagnifierWindow closeEvent
        :return:
        """
        self.closing.emit(QCloseEvent)
