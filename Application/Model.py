import cv2 as opencv
import numpy


class Model(object):
    def __init__(self):
        self.originalImage = None
        self.processedImage = None

    def loadOriginalImage(self, filename, readFlag):
        self.originalImage = opencv.imread(filename, readFlag)