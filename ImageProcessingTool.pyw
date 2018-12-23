import sys

from PyQt5 import QtWidgets

from Application.ViewModels.MainVM import MainVM


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainViewModel = MainVM(app)
    sys.exit(app.exec_())
