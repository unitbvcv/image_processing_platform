from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from pyqtgraph import PlotDataItem, PlotWidget


class PlotterWindow(QtWidgets.QMainWindow):

    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        super().__init__(parent, flags)
        self.__setupUi()

    def __setupUi(self):
        self.setObjectName("PlotterWindow")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.labelFunction = QtWidgets.QLabel(self.centralwidget)
        self.labelFunction.setObjectName("labelFunction")
        self.gridLayout.addWidget(self.labelFunction, 0, 0, 1, 1)
        self.comboBoxFunction = QtWidgets.QComboBox(self.centralwidget)
        self.comboBoxFunction.setObjectName("comboBoxFunction")
        self.gridLayout.addWidget(self.comboBoxFunction, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(613, 20, QtWidgets.QSizePolicy.Expanding,
                                           QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.graphicsView = PlotWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 1, 0, 1, 3)
        self.setCentralWidget(self.centralwidget)

        self.__retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def __retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Plotter"))
        self.labelFunction.setText(_translate("MainWindow", "Plot function:"))

    def closeEvent(self, *args, **kwargs):
        self.graphicsView.getPlotItem().clear()
        # TODO: reset zoom if possible (pls)