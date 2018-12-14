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

        # show the main window
        self._view.show()
