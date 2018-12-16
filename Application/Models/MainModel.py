from dataclasses import dataclass
import cv2 as opencv


@dataclass
class MainModel(object):
    originalImage = None
    processedImage = None
    # TODO: whytf is this here?
    # TODO: because i need it in basic plotting algorithms
    clickPosition = None

    def readOriginalImage(self, filePath: str, asGrayscale: bool):
        if asGrayscale:
            self.originalImage = opencv.imread(filePath, opencv.IMREAD_GRAYSCALE)
        else:
            self.originalImage = opencv.imread(filePath, opencv.IMREAD_COLOR)
            self.originalImage = opencv.cvtColor(self.originalImage, opencv.COLOR_BGR2RGB)

    def saveProcessedImage(self, filePath : str):
        # i think it need to be converted from RGB to BGR
        opencv.imwrite(filePath, opencv.cvtColor(self.processedImage, opencv.COLOR_RGB2BGR))
