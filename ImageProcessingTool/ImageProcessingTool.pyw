from PyQt5 import QtWidgets
from MyWindows import MainWindow

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mymainWindow = MainWindow.MainWindow()
    mymainWindow.show()
    sys.exit(app.exec_())
