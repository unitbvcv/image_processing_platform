from Application.View import MagnifierWindow, MainWindow, PlotterWindow
from PyQt5 import QtCore


class Controller(object):
    def __init__(self):
        # instantiate the QMainWindow objects
        self.mainWindow = MainWindow()
        self.plotterWindow = PlotterWindow(self.mainWindow)
        self.magnifierWindow = MagnifierWindow(self.mainWindow)

        # connect the actions to methods
        self.mainWindow.actionExit.triggered.connect(self.actionExit)
        self.mainWindow.actionInvert.triggered.connect(self.actionInvert)
        self.mainWindow.actionLoadColorImage.triggered.connect(self.actionLoadColorImage)
        self.mainWindow.actionLoadGrayscaleImage.triggered.connect(self.actionLoadColorImage)
        self.mainWindow.actionMagnifier.triggered.connect(self.actionMagnifier)
        self.mainWindow.actionPlotter.triggered.connect(self.actionPlotter)
        self.mainWindow.actionSaveProcessedImage.triggered.connect(self.actionSaveProcessedImage)

        # show the main window
        self.mainWindow.show()

    def actionExit(self):
        QtCore.QCoreApplication.quit()

    def actionInvert(self):
        # TODO
        pass

    def actionLoadColorImage(self):
        # TODO
        pass

    def actionLoadGrayscaleImage(self):
        # TODO
        pass

    def actionMagnifier(self):
        # TODO
        self.magnifierWindow.show()

    def actionPlotter(self):
        # TODO
        self.plotterWindow.show()

    def actionSaveProcessedImage(self):
        # TODO
        pass
