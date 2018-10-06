from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi

class PlotterWindow(QtWidgets.QWidget):

    def __init__(self, parent = None, flags = Qt.WindowFlags()):
        super().__init__(parent, flags)
        loadUi("UI/PlotterWindow.ui", self)
