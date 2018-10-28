from PyQt5 import QtWidgets
from Application.ViewModels import Controller, MainViewModel
import sys

from Application.ViewModels import MagnifierWindowViewModel

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller.Controller()

    # test code
    # a = MagnifierWindowViewModel()
    # a.showWindow()

    b = MainViewModel()

    sys.exit(app.exec_())
