from PyQt5 import QtWidgets
from Application.Controllers import Controller
import sys

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller.Controller()
    sys.exit(app.exec_())
