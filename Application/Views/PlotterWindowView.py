from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget

import Application.Settings


class PlotterWindowView(QtWidgets.QMainWindow):
    """
    TODO: document PlotterWindow
    """

    closing = QtCore.pyqtSignal(QtGui.QCloseEvent, name='closing')

    def __init__(self, parent=None):
        """
        TODO: document PlotterWindow constructor
        :param parent:
        """
        super().__init__(parent)
        self._setupUi()

    def _setupUi(self):
        """
        TODO: document PlotterWindow _setupUi
        :return:
        """
        self.setObjectName("PlotterWindow")
        self.resize(1200, 604)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBoxOriginalImage = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxOriginalImage.setObjectName("groupBoxOriginalImage")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBoxOriginalImage)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.graphicsViewOriginalImage = PlotWidget(self.groupBoxOriginalImage)
        self.graphicsViewOriginalImage.setObjectName("graphicsViewOriginalImage")
        self.horizontalLayout_2.addWidget(self.graphicsViewOriginalImage)
        self.horizontalLayout.addWidget(self.groupBoxOriginalImage)
        self.verticalLayoutSettings = QtWidgets.QVBoxLayout()
        self.verticalLayoutSettings.setObjectName("verticalLayoutSettings")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutSettings.addItem(spacerItem)
        self.groupBoxSettings = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxSettings.setObjectName("groupBoxSettings")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBoxSettings)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.labelFunction = QtWidgets.QLabel(self.groupBoxSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelFunction.sizePolicy().hasHeightForWidth())
        self.labelFunction.setSizePolicy(sizePolicy)
        self.labelFunction.setAlignment(QtCore.Qt.AlignCenter)
        self.labelFunction.setObjectName("labelFunction")
        self.verticalLayout_5.addWidget(self.labelFunction)
        self.comboBoxFunction = QtWidgets.QComboBox(self.groupBoxSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxFunction.sizePolicy().hasHeightForWidth())
        self.comboBoxFunction.setSizePolicy(sizePolicy)
        self.comboBoxFunction.addItems(
            [item.value[1] for item in Application.Settings.PlotterWindowSettings.Functions])
        self.comboBoxFunction.setObjectName("comboBoxFunction")
        self.verticalLayout_5.addWidget(self.comboBoxFunction)
        self.labelVisibleOriginalImage = QtWidgets.QLabel(self.groupBoxSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelVisibleOriginalImage.sizePolicy().hasHeightForWidth())
        self.labelVisibleOriginalImage.setSizePolicy(sizePolicy)
        self.labelVisibleOriginalImage.setAlignment(QtCore.Qt.AlignCenter)
        self.labelVisibleOriginalImage.setObjectName("labelVisibleOriginalImage")
        self.verticalLayout_5.addWidget(self.labelVisibleOriginalImage)
        self.listWidgetVisibleOriginalImage = QtWidgets.QListWidget(self.groupBoxSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetVisibleOriginalImage.sizePolicy().hasHeightForWidth())
        self.listWidgetVisibleOriginalImage.setSizePolicy(sizePolicy)
        self.listWidgetVisibleOriginalImage.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidgetVisibleOriginalImage.setProperty("showDropIndicator", False)
        self.listWidgetVisibleOriginalImage.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.listWidgetVisibleOriginalImage.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidgetVisibleOriginalImage.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.listWidgetVisibleOriginalImage.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.listWidgetVisibleOriginalImage.setUniformItemSizes(False)
        self.listWidgetVisibleOriginalImage.setObjectName("listWidgetVisibleOriginalImage")
        self.verticalLayout_5.addWidget(self.listWidgetVisibleOriginalImage)
        self.labelVisibleProcessedImage = QtWidgets.QLabel(self.groupBoxSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelVisibleProcessedImage.sizePolicy().hasHeightForWidth())
        self.labelVisibleProcessedImage.setSizePolicy(sizePolicy)
        self.labelVisibleProcessedImage.setAlignment(QtCore.Qt.AlignCenter)
        self.labelVisibleProcessedImage.setObjectName("labelVisibleProcessedImage")
        self.verticalLayout_5.addWidget(self.labelVisibleProcessedImage)
        self.listWidgetVisibleProcessedImage = QtWidgets.QListWidget(self.groupBoxSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetVisibleProcessedImage.sizePolicy().hasHeightForWidth())
        self.listWidgetVisibleProcessedImage.setSizePolicy(sizePolicy)
        self.listWidgetVisibleProcessedImage.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidgetVisibleProcessedImage.setProperty("showDropIndicator", False)
        self.listWidgetVisibleProcessedImage.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.listWidgetVisibleProcessedImage.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.listWidgetVisibleProcessedImage.setObjectName("listWidgetVisibleProcessedImage")
        self.verticalLayout_5.addWidget(self.listWidgetVisibleProcessedImage)
        self.horizontalAutoScaleAndCenterOnChange = QtWidgets.QHBoxLayout()
        self.horizontalAutoScaleAndCenterOnChange.setObjectName("horizontalAutoScaleAndCenterOnChange")
        spacerItem1 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalAutoScaleAndCenterOnChange.addItem(spacerItem1)
        self.checkBoxAutoScaleAndCenterOnChange = QtWidgets.QCheckBox(self.groupBoxSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBoxAutoScaleAndCenterOnChange.sizePolicy().hasHeightForWidth())
        self.checkBoxAutoScaleAndCenterOnChange.setSizePolicy(sizePolicy)
        self.checkBoxAutoScaleAndCenterOnChange.setChecked(True)
        self.checkBoxAutoScaleAndCenterOnChange.setObjectName("checkBoxAutoScaleAndCenterOnChange")
        self.horizontalAutoScaleAndCenterOnChange.addWidget(self.checkBoxAutoScaleAndCenterOnChange)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Minimum)
        self.horizontalAutoScaleAndCenterOnChange.addItem(spacerItem2)
        self.verticalLayout_5.addLayout(self.horizontalAutoScaleAndCenterOnChange)
        self.pushButtonScaleAndCenter = QtWidgets.QPushButton(self.groupBoxSettings)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonScaleAndCenter.sizePolicy().hasHeightForWidth())
        self.pushButtonScaleAndCenter.setSizePolicy(sizePolicy)
        self.pushButtonScaleAndCenter.setObjectName("pushButtonScaleAndCenter")
        self.verticalLayout_5.addWidget(self.pushButtonScaleAndCenter)
        self.verticalLayoutSettings.addWidget(self.groupBoxSettings)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayoutSettings.addItem(spacerItem3)
        self.horizontalLayout.addLayout(self.verticalLayoutSettings)
        self.groupBoxProcessedImage = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxProcessedImage.setObjectName("groupBoxProcessedImage")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBoxProcessedImage)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.graphicsViewProcessedImage = PlotWidget(self.groupBoxProcessedImage)
        self.graphicsViewProcessedImage.setObjectName("graphicsViewProcessedImage")
        self.horizontalLayout_3.addWidget(self.graphicsViewProcessedImage)
        self.horizontalLayout.addWidget(self.groupBoxProcessedImage)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.setCentralWidget(self.centralwidget)

        # Setting plotter
        self.plotItemOriginalImage.setMenuEnabled(False)
        self.plotItemProcessedImage.setMenuEnabled(False)
        self.plotItemOriginalImage.addLegend()
        self.plotItemProcessedImage.addLegend()
        self.plotItemOriginalImage.showGrid(x=True, y=True, alpha=1.0)
        self.plotItemProcessedImage.showGrid(x=True, y=True, alpha=1.0)
        self.graphicsViewOriginalImage.setXLink(self.graphicsViewProcessedImage)
        self.graphicsViewOriginalImage.setYLink(self.graphicsViewProcessedImage)

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def _retranslateUi(self):
        """
        TODO: document PlotterWindow _retranslateUi
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("PlotterWindow", "Plotter"))
        self.groupBoxOriginalImage.setTitle(_translate("PlotterWindow", "Original image"))
        self.groupBoxSettings.setTitle(_translate("PlotterWindow", "Settings"))
        self.labelFunction.setText(_translate("PlotterWindow", "Plot function"))
        self.labelVisibleOriginalImage.setText(_translate("PlotterWindow", "Visible original image plots"))
        self.labelVisibleProcessedImage.setText(_translate("PlotterWindow", "Visible processed image plots"))
        self.checkBoxAutoScaleAndCenterOnChange.setText(
            _translate("PlotterWindow", "Auto scale and center plots on change"))
        self.pushButtonScaleAndCenter.setText(_translate("PlotterWindow", "Scale and center plots to view"))
        self.groupBoxProcessedImage.setTitle(_translate("PlotterWindow", "Processed image"))

    def closeEvent(self, QCloseEvent):
        """
        TODO: document PlotterWindow closeEvent
        :param QCloseEvent:
        :return:
        """
        self.closing.emit(QCloseEvent)

    @property
    def plotItemOriginalImage(self):
        """
        TODO: document PlotterWindow originalPlotItem
        :return:
        """
        return self.graphicsViewOriginalImage.plotItem

    @property
    def plotItemProcessedImage(self):
        """
        TODO: document PlotterWindow processedPlotItem
        :return:
        """
        return self.graphicsViewProcessedImage.plotItem

    def scaleAndCenterToPlots(self, plots):
        """
        TODO document PlotterWindow _scaleAndCenterPlots
        :param plots:
        :return:
        """
        # if the list of dataitems the plotitem will autorange based off is empty
        # the plot will behave weirdly on autorange
        if len(plots) > 0:
            self.plotItemOriginalImage.getViewBox().autoRange(items=plots)
            self.plotItemProcessedImage.getViewBox().autoRange(items=plots)

    def addPlotDataItems(self, plotItem, plotDataItems):
        """
        TODO: document PlotterWindow _addPlotDataItems
        :param plotItem:
        :param plotDataItems:
        :return:
        """
        for plotDataItem in plotDataItems:
            plotItem.addItem(plotDataItem)

    def removePlotDataItems(self, plotItem, plotDataItems):
        """
        TODO: document PlotterWindow _removePlotDataItems
        :param plotItem:
        :param plotDataItems:
        :return:
        """
        for plotDataItem in plotDataItems:
            plotItem.legend.removeItem(plotDataItem.name())
            plotItem.removeItem(plotDataItem)

    def clearPlotItems(self):
        """
        TODO: document PlotterWindow clearPlotItems
        :return:
        """
        self.plotItemOriginalImage.clear()
        self.plotItemProcessedImage.clear()

    def clearPlotItemsLegends(self, originalImageKeys, processedImageKeys):
        """
        TODO: document PlotterWindow clearPlotItemsLegends
        :param originalImageKeys:
        :param processedImageKeys:
        :return:
        """
        for item in self.plotItemOriginalImage.legend.items:
            self.plotItemOriginalImage.legend.removeItem(item)

        for item in self.plotItemProcessedImage.legend.items:
            self.plotItemProcessedImage.legend.removeItem(item)

        # for legendString in originalImageKeys:
        #     self.plotItemOriginalImage.legend.removeItem(legendString)
        #
        # for legendString in processedImageKeys:
        #     self.plotItemProcessedImage.legend.removeItem(legendString)

    def clearListWidgets(self):
        """
        TODO: document PlotterWindow clearListWidgets
        :return:
        """
        self.listWidgetVisibleOriginalImage.clear()
        self.listWidgetVisibleProcessedImage.clear()

    def populateListWidgets(self, originalImageItems, processedImageItems):
        """
        TODO: document PlotterWindow populateListWidgets
        :param originalImageItems:
        :param processedImageItems:
        :return:
        """
        self.listWidgetVisibleOriginalImage.addItems(originalImageItems)
        self.listWidgetVisibleProcessedImage.addItems(processedImageItems)
