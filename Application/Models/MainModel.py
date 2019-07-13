from collections import deque
import cv2 as opencv
from dataclasses import dataclass
import numpy as np

import Application.Settings


@dataclass
class MainModel(object):
    originalImage = None
    _processedImage = None
    leftClickPosition = None
    rightClickLastPositions = deque(maxlen=Application.Settings.RightClickPointerSettings.numberOfClicksToRemember)

    @property
    def processedImage(self):
        return self._processedImage

    @processedImage.setter
    def processedImage(self, value):
        if value is not None:
            if value.base is not None:
                value = value.copy()
        self._processedImage = value

    def readOriginalImage(self, filePath: str, asGrayscale: bool):
        if asGrayscale:
            self.originalImage = opencv.imread(filePath, opencv.IMREAD_GRAYSCALE)
        else:
            self.originalImage = opencv.imread(filePath, opencv.IMREAD_COLOR)
            self.originalImage = opencv.cvtColor(self.originalImage, opencv.COLOR_BGR2RGB)

    def reset(self):
        self.originalImage = None
        self.processedImage = None
        self.leftClickPosition = None
        self.rightClickLastPositions.clear()

    def saveProcessedImage(self, filePath: str):
        if self.processedImage is not None:
            processedImageShapeLen = len(self.processedImage.shape)

            if processedImageShapeLen == 2:
                opencv.imwrite(filePath, self.processedImage)
            elif processedImageShapeLen == 3:
                opencv.imwrite(filePath, opencv.cvtColor(self.processedImage, opencv.COLOR_RGB2BGR))
