import re

from PyQt5 import QtCore, QtGui, QtWidgets

import Application.Settings
import Application.Utils.ZoomOperations
from Application.Views.MainWindowImageLabel import MainWindowImageLabel


class MainWindowView(QtWidgets.QMainWindow):
    @property
    def zoom(self):
        return self._zoom

    def __init__(self):
        super().__init__()

        # Python doesn't like properties on variables that are created in a function that's not __init__
        # so we create it here
        self._zoom = 1.0

        self._setupUi()
        self._setupImageLabels()
        self._setupMenuCornerWidget()
        self._setupZoomFunctionality()

        # synchronize the scrollbars of the scrollAreas
        self.scrollAreaOriginalImage.horizontalScrollBar().valueChanged.connect(
            self.scrollAreaProcessedImage.horizontalScrollBar().setValue)
        self.scrollAreaProcessedImage.horizontalScrollBar().valueChanged.connect(
            self.scrollAreaOriginalImage.horizontalScrollBar().setValue)

        self.scrollAreaOriginalImage.verticalScrollBar().valueChanged.connect(
            self.scrollAreaProcessedImage.verticalScrollBar().setValue)
        self.scrollAreaProcessedImage.verticalScrollBar().valueChanged.connect(
            self.scrollAreaOriginalImage.verticalScrollBar().setValue)

        # connect signals to slots
        self.labelOriginalImage.mouseLeavedSignal.connect(self._mouseLeavedEvent)
        self.labelProcessedImage.mouseLeavedSignal.connect(self._mouseLeavedEvent)
        self.labelOriginalImage.finishedPaintingSignal.connect(self._labelFinishedPaintingEvent)
        self.labelProcessedImage.finishedPaintingSignal.connect(self._labelFinishedPaintingEvent)

        # define necessary data for menu API
        self._menusDictionary = {
            self.menuFile.title(): self.menuFile,
            self.menuTools.title(): self.menuTools
        }

        self._menuActionsDictionary = {
            self.actionLoadGrayscaleImage.text(): self.actionLoadGrayscaleImage,
            self.actionLoadColorImage.text(): self.actionLoadColorImage,
            self.actionSaveProcessedImage.text(): self.actionSaveProcessedImage,
            self.actionExit.text(): self.actionExit,
            self.actionMagnifier.text(): self.actionMagnifier,
            self.actionPlotter.text(): self.actionPlotter
        }

# region WINDOW SET UP

    def _setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(1024, 768)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayoutImages = QtWidgets.QHBoxLayout()
        self.horizontalLayoutImages.setSpacing(6)
        self.horizontalLayoutImages.setObjectName("horizontalLayoutImages")
        self.groupBoxOriginalImage = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxOriginalImage.sizePolicy().hasHeightForWidth())
        self.groupBoxOriginalImage.setSizePolicy(sizePolicy)
        self.groupBoxOriginalImage.setObjectName("groupBoxOriginalImage")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBoxOriginalImage)
        self.horizontalLayout.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.scrollAreaOriginalImage = QtWidgets.QScrollArea(self.groupBoxOriginalImage)
        self.scrollAreaOriginalImage.setStyleSheet("")
        self.scrollAreaOriginalImage.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollAreaOriginalImage.setWidgetResizable(True)
        self.scrollAreaOriginalImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollAreaOriginalImage.setObjectName("scrollAreaOriginalImage")
        self.scrollAreaWidgetOriginalImage = QtWidgets.QWidget()
        self.scrollAreaWidgetOriginalImage.setGeometry(QtCore.QRect(0, 0, 471, 568))
        self.scrollAreaWidgetOriginalImage.setObjectName("scrollAreaWidgetOriginalImage")
        self.scrollAreaOriginalImage.setWidget(self.scrollAreaWidgetOriginalImage)
        self.horizontalLayout.addWidget(self.scrollAreaOriginalImage)
        self.horizontalLayoutImages.addWidget(self.groupBoxOriginalImage)
        self.groupBoxProcessedImage = QtWidgets.QGroupBox(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxProcessedImage.sizePolicy().hasHeightForWidth())
        self.groupBoxProcessedImage.setSizePolicy(sizePolicy)
        self.groupBoxProcessedImage.setObjectName("groupBoxProcessedImage")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBoxProcessedImage)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scrollAreaProcessedImage = QtWidgets.QScrollArea(self.groupBoxProcessedImage)
        self.scrollAreaProcessedImage.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollAreaProcessedImage.setWidgetResizable(True)
        self.scrollAreaProcessedImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.scrollAreaProcessedImage.setObjectName("scrollAreaProcessedImage")
        self.scrollAreaWidgetProcessedImage = QtWidgets.QWidget()
        self.scrollAreaWidgetProcessedImage.setGeometry(QtCore.QRect(0, 0, 470, 568))
        self.scrollAreaWidgetProcessedImage.setObjectName("scrollAreaWidgetProcessedImage")
        self.scrollAreaProcessedImage.setWidget(self.scrollAreaWidgetProcessedImage)
        self.horizontalLayout_2.addWidget(self.scrollAreaProcessedImage)
        self.horizontalLayoutImages.addWidget(self.groupBoxProcessedImage)
        self.verticalLayout.addLayout(self.horizontalLayoutImages)
        self.horizontalLayoutZoom = QtWidgets.QHBoxLayout()
        self.horizontalLayoutZoom.setSpacing(6)
        self.horizontalLayoutZoom.setObjectName("horizontalLayoutZoom")
        self.buttonResetZoom = QtWidgets.QPushButton(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonResetZoom.sizePolicy().hasHeightForWidth())
        self.buttonResetZoom.setSizePolicy(sizePolicy)
        self.buttonResetZoom.setMinimumSize(QtCore.QSize(0, 33))
        self.buttonResetZoom.setObjectName("buttonResetZoom")
        self.horizontalLayoutZoom.addWidget(self.buttonResetZoom)
        self.horizontalSliderZoom = QtWidgets.QSlider(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalSliderZoom.sizePolicy().hasHeightForWidth())
        self.horizontalSliderZoom.setSizePolicy(sizePolicy)
        self.horizontalSliderZoom.setMinimumSize(QtCore.QSize(0, 33))
        self.horizontalSliderZoom.setMaximum(1)
        self.horizontalSliderZoom.setSingleStep(1)
        self.horizontalSliderZoom.setPageStep(1)
        self.horizontalSliderZoom.setProperty("value", 1)
        self.horizontalSliderZoom.setSliderPosition(1)
        self.horizontalSliderZoom.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderZoom.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSliderZoom.setTickInterval(1)
        self.horizontalSliderZoom.setObjectName("horizontalSliderZoom")
        self.horizontalLayoutZoom.addWidget(self.horizontalSliderZoom)
        self.labelZoomFactor = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelZoomFactor.sizePolicy().hasHeightForWidth())
        self.labelZoomFactor.setSizePolicy(sizePolicy)
        self.labelZoomFactor.setMinimumSize(QtCore.QSize(0, 33))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.labelZoomFactor.setFont(font)
        self.labelZoomFactor.setObjectName("labelZoomFactor")
        self.horizontalLayoutZoom.addWidget(self.labelZoomFactor)
        self.verticalLayout.addLayout(self.horizontalLayoutZoom)
        self.gridLayoutMouseLabels = QtWidgets.QGridLayout()
        self.gridLayoutMouseLabels.setSpacing(6)
        self.gridLayoutMouseLabels.setObjectName("gridLayoutMouseLabels")
        self.labelOriginalImagePixelValue = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelOriginalImagePixelValue.sizePolicy().hasHeightForWidth())
        self.labelOriginalImagePixelValue.setSizePolicy(sizePolicy)
        self.labelOriginalImagePixelValue.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelOriginalImagePixelValue.setFont(font)
        self.labelOriginalImagePixelValue.setText("")
        self.labelOriginalImagePixelValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelOriginalImagePixelValue.setObjectName("labelOriginalImagePixelValue")
        self.gridLayoutMouseLabels.addWidget(self.labelOriginalImagePixelValue, 0, 0, 1, 1)
        self.labelProcessedImagePixelValue = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelProcessedImagePixelValue.sizePolicy().hasHeightForWidth())
        self.labelProcessedImagePixelValue.setSizePolicy(sizePolicy)
        self.labelProcessedImagePixelValue.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelProcessedImagePixelValue.setFont(font)
        self.labelProcessedImagePixelValue.setText("")
        self.labelProcessedImagePixelValue.setAlignment(QtCore.Qt.AlignCenter)
        self.labelProcessedImagePixelValue.setObjectName("labelProcessedImagePixelValue")
        self.gridLayoutMouseLabels.addWidget(self.labelProcessedImagePixelValue, 0, 1, 1, 1)
        self.labelMousePosition = QtWidgets.QLabel(self.centralWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelMousePosition.sizePolicy().hasHeightForWidth())
        self.labelMousePosition.setSizePolicy(sizePolicy)
        self.labelMousePosition.setMinimumSize(QtCore.QSize(0, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.labelMousePosition.setFont(font)
        self.labelMousePosition.setText("")
        self.labelMousePosition.setAlignment(QtCore.Qt.AlignCenter)
        self.labelMousePosition.setObjectName("labelMousePosition")
        self.gridLayoutMouseLabels.addWidget(self.labelMousePosition, 1, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayoutMouseLabels)
        self.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuTools = QtWidgets.QMenu(self.menuBar)
        self.menuTools.setObjectName("menuTools")
        self.setMenuBar(self.menuBar)
        self.actionLoadGrayscaleImage = QtWidgets.QAction(self)
        self.actionLoadGrayscaleImage.setObjectName("actionLoadGrayscaleImage")
        self.actionLoadColorImage = QtWidgets.QAction(self)
        self.actionLoadColorImage.setObjectName("actionLoadColorImage")
        self.actionSaveProcessedImage = QtWidgets.QAction(self)
        self.actionSaveProcessedImage.setObjectName("actionSaveProcessedImage")
        self.actionExit = QtWidgets.QAction(self)
        self.actionExit.setObjectName("actionExit")
        self.actionMagnifier = QtWidgets.QAction(self)
        self.actionMagnifier.setObjectName("actionMagnifier")
        self.actionPlotter = QtWidgets.QAction(self)
        self.actionPlotter.setObjectName("actionPlotter")
        self.menuFile.addAction(self.actionLoadGrayscaleImage)
        self.menuFile.addAction(self.actionLoadColorImage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSaveProcessedImage)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuTools.addAction(self.actionMagnifier)
        self.menuTools.addAction(self.actionPlotter)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuTools.menuAction())

        self._retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

    def _retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Image Processing Tool"))
        self.groupBoxOriginalImage.setTitle(_translate("MainWindow", "Original image"))
        self.groupBoxProcessedImage.setTitle(_translate("MainWindow", "Processed image"))
        self.buttonResetZoom.setText(_translate("MainWindow", "Reset"))
        self.labelZoomFactor.setText(_translate("MainWindow", "1.00x"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuTools.setTitle(_translate("MainWindow", "Tools"))
        self.actionLoadGrayscaleImage.setText(_translate("MainWindow", "Load grayscale image"))
        self.actionLoadColorImage.setText(_translate("MainWindow", "Load color image"))
        self.actionSaveProcessedImage.setText(_translate("MainWindow", "Save processed image"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionMagnifier.setText(_translate("MainWindow", "Magnifier"))
        self.actionPlotter.setText(_translate("MainWindow", "Plotter"))

    def _setupImageLabels(self):
        self.stackedLayoutOriginalImage = QtWidgets.QStackedLayout(self.scrollAreaWidgetOriginalImage)
        self.stackedLayoutProcessedImage = QtWidgets.QStackedLayout(self.scrollAreaWidgetProcessedImage)

        self.labelOriginalImage = MainWindowImageLabel(self.scrollAreaWidgetOriginalImage)
        self.labelOriginalImage.setMouseTracking(True)
        self.labelOriginalImage.setText("")
        self.labelOriginalImage.setScaledContents(False)
        self.labelOriginalImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelOriginalImage.setObjectName("labelOriginalImage")
        self.labelOriginalImage.setGeometry(0, 0, 0, 0)

        self.labelProcessedImage = MainWindowImageLabel(self.scrollAreaWidgetProcessedImage)
        self.labelProcessedImage.setMouseTracking(True)
        self.labelProcessedImage.setText("")
        self.labelProcessedImage.setScaledContents(False)
        self.labelProcessedImage.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.labelProcessedImage.setObjectName("labelProcessedImage")
        self.labelProcessedImage.setGeometry(0, 0, 0, 0)

        self.stackedLayoutOriginalImage.addWidget(self.labelOriginalImage)
        self.stackedLayoutProcessedImage.addWidget(self.labelProcessedImage)

    def _setupMenuCornerWidget(self):
        self.rightMenuBar = QtWidgets.QMenuBar()
        self.menuBar.setCornerWidget(self.rightMenuBar)
        self.actionSaveAsOriginalImage = QtWidgets.QAction(self)
        self.actionSaveAsOriginalImage.setObjectName("actionSaveAsOriginalImage")
        self.rightMenuBar.addAction(self.actionSaveAsOriginalImage)

        _translate = QtCore.QCoreApplication.translate
        self.actionSaveAsOriginalImage.setText(_translate("MainWindow", "Save as original image"))

    def _setupZoomFunctionality(self):
        # connect the zoom option
        self.horizontalSliderZoom.setMinimum(
            Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
                Application.Settings.MainWindowSettings.zoomMinimumValue))
        self.horizontalSliderZoom.setMaximum(
            Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
                Application.Settings.MainWindowSettings.zoomMaximumValue))
        self.horizontalSliderZoom.setSingleStep(
            Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
                Application.Settings.MainWindowSettings.zoomSingleStep))
        self.horizontalSliderZoom.setPageStep(
            Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
                Application.Settings.MainWindowSettings.zoomPageStep))
        self.horizontalSliderZoom.setTickInterval(
            Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
                Application.Settings.MainWindowSettings.ticksInterval)
        )

        self._zoom = Application.Settings.MainWindowSettings.zoomDefaultValue
        self.horizontalSliderZoom.setValue(Application.Utils.ZoomOperations.calculateSliderValueFromZoom(self._zoom))
        self.horizontalSliderZoom.valueChanged.connect(self._zoomValueChangedEvent)
        self.buttonResetZoom.pressed.connect(self.zoomValueResetEvent)

# endregion

# region MENU API

    def addMenu(self, menuName, menuPath=None, beforeElementName=None):
        """
        Adds a QMenu in the deepest menu given in menuPath with the title and objectName menuName before the element
        with the identifier beforeElementName. Parameter menuName will be used as key to identify the menu afterwards.
        If it already exists or menuName is None or path is invalid, it does nothing - no matter in which other menu
        the name is already used.
        If the sub-menus along the path do not exist, they will be created (appending them in their corresponding menu).
        Path is invalid if a menu with the same name already exists when new menus are being created.
        If menuPath is not given, the menu will be added in the top menu bar.
        If beforeElementName is not specified or is not found or is not valid (present in the menu), the menu is added
        as the last element.

        Examples of paths:
            - 'Foo/Bar'
            - 'Foo\\Bar'
            - r'Foo\Bar'

        Example of invalid path:
            - 'File/Submenu/File'

        :param menuName: string
        :param menuPath: string; default value: None
        :param beforeElementName: string; default value: None
        :return: None
        """

        def _addMenu(menuName, menu, beforeAction):
            newMenu = QtWidgets.QMenu(menu)
            newMenu.setTitle(QtCore.QCoreApplication.translate("MainWindow", menuName))
            newMenu.setObjectName(menuName)
            self._menusDictionary[menuName] = newMenu
            menu.insertAction(beforeAction, newMenu.menuAction())

        if menuName is not None and menuName not in self._menusDictionary:
            beforeElementAction = None
            if beforeElementName in self._menuActionsDictionary:
                beforeElementAction = self._menuActionsDictionary[beforeElementName]
            elif beforeElementName in self._menusDictionary:
                beforeElementAction = self._menusDictionary[beforeElementName].menuAction()

            currentMenu = self.menuBar
            if menuPath is not None:
                menuNames = re.split(r'[/\\]', menuPath)

                # traverse the path to the deepest submenu; create them along the way if they don't exist
                startedNonExistingMenusPath = False
                for currentSubMenuName in menuNames:
                    if startedNonExistingMenusPath is False:
                        if currentSubMenuName not in self._menusDictionary:
                            _addMenu(currentSubMenuName, currentMenu, beforeElementAction)
                            startedNonExistingMenusPath = True
                        elif self._menusDictionary[currentSubMenuName].menuAction() not in currentMenu.actions():
                            return
                    else:
                        if currentSubMenuName in self._menusDictionary:
                            return
                        _addMenu(currentSubMenuName, currentMenu, beforeElementAction)

                    currentMenu = self._menusDictionary[currentSubMenuName]

            # here the deepest submenu and insertion point have been found
            _addMenu(menuName, currentMenu, beforeElementAction)

    def addMenuAction(self, actionName, menuPath, beforeElementName=None):
        """
        Adds a QAction to the deepest menu in the menuPath with the title and objectName actionName before the element
        with the identifier beforeElementName. Parameter actionName will be used as key to identify the menu afterwards.
        If it already exists or menuPath is None or actionName is None or path is invalid, it does nothing - no matter
        in which other menu the name is already used.
        If the sub-menus along the path do not exist, they will be created (appending them in their corresponding menu).
        Path is invalid if a menu with the same name already exists when new menus are being created.
        If beforeElementName is not specified or is not found or is not valid (present in the menu), the action is added
        as the last element.

        :param actionName: string
        :param menuPath: string
        :param beforeElementName: string; default value: None
        :return: None
        """

        def _addAction(actionName, menu, beforeAction):
            newAction = QtWidgets.QAction(self)
            newAction.setObjectName(actionName)
            newAction.setText(QtCore.QCoreApplication.translate("MainWindow", actionName))
            menu.insertAction(beforeAction, newAction)
            self._menuActionsDictionary[actionName] = newAction

        if actionName is not None and actionName not in self._menuActionsDictionary:
            beforeElementAction = None
            if beforeElementName in self._menuActionsDictionary:
                beforeElementAction = self._menuActionsDictionary[beforeElementName]
            elif beforeElementName in self._menusDictionary:
                beforeElementAction = self._menusDictionary[beforeElementName].menuAction()

            if menuPath is not None:
                menuNames = re.split(r'[/\\]', menuPath)
                lastMenuName = menuNames[-1]

                if lastMenuName not in self._menusDictionary:
                    self.addMenu(lastMenuName, '/'.join(menuNames[:-1]))

                    if lastMenuName not in self._menusDictionary:
                        return  # invalid path

                menu = self._menusDictionary[lastMenuName]
                _addAction(actionName, menu, beforeElementAction)


    # def addMenuSeparator(self, menuName, beforeActionName=None):
    #     """
    #     Adds a separator in the menuName [before beforeActionName].
    #     It does nothing if the menuName is not found.
    #     If beforeActionName is not found, it appends the new action.
    #     :param menuName: string
    #     :param beforeActionName: string; default value: None
    #     :return: None
    #     """
    #     if menuName in self._menusDictionary:
    #         beforeAction = None
    #         if beforeActionName is not None:
    #             beforeAction = self._menuActionsDictionary[beforeActionName]
    #         self._menusDictionary[menuName].insertSeparator(beforeAction)

# endregion

    def _mouseLeavedEvent(self, QEvent):
        self.labelMousePosition.setText('')
        self.labelOriginalImagePixelValue.setText('')
        self.labelProcessedImagePixelValue.setText('')

    def _labelFinishedPaintingEvent(self):
        # here we can synchronize scrollbars, after the paint event has finished
        # before paint event, the scrollbars don't exist
        self.scrollAreaProcessedImage.horizontalScrollBar().setValue(
            self.scrollAreaOriginalImage.horizontalScrollBar().value())

        self.scrollAreaProcessedImage.verticalScrollBar().setValue(
            self.scrollAreaOriginalImage.verticalScrollBar().value())

    def closeEvent(self, QCloseEvent):
        QtCore.QCoreApplication.quit()

# region ZOOM FUNCTIONALITY

    def zoomValueResetEvent(self):
        sliderValue = Application.Utils.ZoomOperations.calculateSliderValueFromZoom(
            Application.Settings.MainWindowSettings.zoomDefaultValue)
        self.horizontalSliderZoom.setValue(sliderValue)
        self._zoomValueChangedEvent(sliderValue)

    def _zoomValueChangedEvent(self, value):
        self._zoom = Application.Utils.ZoomOperations.calculateZoomFromSliderValue(value)
        self.labelZoomFactor.setText(f"{self._zoom:.2f}x")
        self._setZoom()

    def _setZoom(self):
        self.labelOriginalImage.setZoom(self._zoom)
        self.labelProcessedImage.setZoom(self._zoom)

# endregion
