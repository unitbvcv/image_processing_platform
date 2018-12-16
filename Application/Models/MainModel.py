from dataclasses import dataclass
import cv2 as opencv


@dataclass
class MainModel(object):
    originalImage = None
    processedImage = None
    clickPosition = None

    def readOriginalImage(self, filePath: str, asGrayscale: bool):
        if asGrayscale:
            self.originalImage = opencv.imread(filePath, opencv.IMREAD_GRAYSCALE)
        else:
            self.originalImage = opencv.imread(filePath, opencv.IMREAD_COLOR)
            self.originalImage = opencv.cvtColor(self.originalImage, opencv.COLOR_BGR2RGB)

    def saveProcessedImage(self, filePath : str):
        if self.processedImage:
            opencv.imwrite(filePath, opencv.cvtColor(self.processedImage, opencv.COLOR_RGB2BGR))
