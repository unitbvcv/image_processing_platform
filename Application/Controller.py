from PyQt5 import QtWidgets
from Application.GeneratedUI import Ui_MagnifierWindow, Ui_MainWindow, Ui_PlotterWindow

class Controller(object):
    def __init__(self):
        # instantiate the QMainWindow objects
        self.mainWindow = QtWidgets.QMainWindow()
        self.plotterWindow = QtWidgets.QMainWindow(self.mainWindow)
        self.magnifierWindow = QtWidgets.QMainWindow(self.mainWindow)

        # instantiate the objects that hold the UI design
        self.ui_mainWindow = Ui_MainWindow()
        self.ui_plotterWindow = Ui_PlotterWindow()
        self.ui_magnifierWindow = Ui_MagnifierWindow()

        # run the UI setup
        self.__setupUi()
        self.__retranslateUi()

        # show the main window
        self.mainWindow.show()

    def __setupUi(self):
        self.ui_mainWindow.setupUi(self.mainWindow)
        self.ui_plotterWindow.setupUi(self.plotterWindow)
        self.ui_magnifierWindow.setupUi(self.magnifierWindow)

    def __retranslateUi(self):
        self.ui_mainWindow.retranslateUi(self.mainWindow)
        self.ui_plotterWindow.retranslateUi(self.mainWindow)
        self.ui_magnifierWindow.retranslateUi(self.mainWindow)
