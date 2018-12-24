from sys import exc_info

from PyQt5 import QtCore, QtWidgets


class SmartDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self._setBasicUI()

        self._cancelled = None
        self._readData = None

        self._textBoxDictionary = {}

    def _setBasicUI(self):
        self.setWindowTitle("Input dialog")
        self.setMinimumWidth(250)
        self.setMaximumHeight(500)

        self.baseLayout = QtWidgets.QVBoxLayout(self)
        self.baseLayout.setContentsMargins(11, 11, 11, 11)
        self.baseLayout.setSpacing(6)
        self.baseLayout.setObjectName("baseLayout")

        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)

        self.scrollAreaWidget = QtWidgets.QWidget()
        self.scrollAreaWidget.setGeometry(QtCore.QRect(0, 0, 300, 200))
        self.scrollAreaWidget.setMinimumWidth(170)
        self.scrollAreaWidget.setObjectName("scrollAreaWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.scrollAreaWidget)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName("gridLayout")

        self.scrollArea.setWidget(self.scrollAreaWidget)
        self.baseLayout.addWidget(self.scrollArea)

        # Add buttons Ok & Cancel
        self.horizontalButtonLayout = QtWidgets.QHBoxLayout()
        self.horizontalButtonLayout.setSpacing(6)
        self.horizontalButtonLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalButtonLayout.setObjectName("horizontalButtonLayout")

        self.okButton = QtWidgets.QPushButton(self)
        self.okButton.setFixedWidth(75)
        self.okButton.setText("Ok")
        self.okButton.clicked.connect(self.accept)
        self.horizontalButtonLayout.addWidget(self.okButton, QtCore.Qt.AlignCenter)

        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setFixedWidth(75)
        self.cancelButton.setText("Cancel")
        self.cancelButton.clicked.connect(self.reject)
        self.horizontalButtonLayout.addWidget(self.cancelButton, QtCore.Qt.AlignCenter)

        self.baseLayout.addLayout(self.horizontalButtonLayout)

    @property
    def cancelled(self):
        return self._cancelled

    @property
    def readData(self):
        return self._readData

    def showDialog(self, **kwargs):
        # designing dialog
        # TODO: move font size and everything in settings
        for paramName, value in kwargs.items():
            if isinstance(value, tuple):
                assert len(value) == 2
                labelText = value[0]
            else:
                labelText = paramName

            row = self.gridLayout.rowCount()
            label = QtWidgets.QLabel(self.scrollAreaWidget)
            label.setText(labelText)
            font = label.font()
            font.setPointSize(11)
            label.setFont(font)
            label.setAlignment(QtCore.Qt.AlignLeft)
            self.gridLayout.addWidget(label, row, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

            textBox = QtWidgets.QLineEdit(self.scrollAreaWidget)
            textBox.setFont(font)
            self.gridLayout.addWidget(textBox, row, 1)
            self._textBoxDictionary[paramName] = textBox

        # showing dialog
        if self.exec() == QtWidgets.QDialog.Rejected:
            self._cancelled = True
            return

        # the dialog was accepted
        self._cancelled = False
        self._readData = {}

        for paramName, value in kwargs.items():
            if isinstance(value, tuple):
                typeRequested = value[1]
            else:
                typeRequested = value

            try:
                convertedValue = typeRequested(self._textBoxDictionary[paramName].text())
                self._readData[paramName] = convertedValue
            except:
                exceptionInfo = exc_info()
                QtWidgets.QMessageBox.critical(
                    None,
                    'InputDialog error',
                    f'Conversion error for parameter {paramName}. Exception raised:\n'
                    f'{exceptionInfo[0].__name__}: {exceptionInfo[1]}'
                )
                self._cancelled = True
                return
