from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import MyWindows.PlotterWindow.PlotterWindow

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        super().__init__(parent, flags)
        loadUi("UI/MainWindow.ui", self)

        # Add "Save as original image" button to the right of the menuBar
        self.rightMenuBar = QtWidgets.QMenuBar(self.menuBar)
        # TODO: add connection for action
        self.rightMenuBar.addAction("Save as original image")
        self.menuBar.setCornerWidget(self.rightMenuBar)

        self.actionPlotter.triggered.connect(self.openPlotter)

    def openPlotter(self):
        plotterWindow = PlotterWindow()
        plotterWindow.show()
