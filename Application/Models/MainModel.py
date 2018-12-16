from dataclasses import dataclass
import cv2 as opencv


@dataclass
class MainModel(object):
    originalImage = None
    processedImage = None
    # TODO: whytf is this here?
    clickPosition = None

    def readOriginalImage(self, filePath : str, asGrayscale : bool):
        if asGrayscale:
            self.originalImage = opencv.imread(filePath, opencv.IMREAD_GRAYSCALE)
        else:
            self.originalImage = opencv.imread(filePath, opencv.IMREAD_COLOR)

    def saveProcessedImage(self, filePath : str):
        opencv.imwrite(filePath, self.processedImage)
