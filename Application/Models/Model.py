import cv2 as opencv

"""
Pre clasa
"""
class Model(object):
    def __init__(self):
        """
        Constructor
        """
        self.originalImage = None
        self.processedImage = None

    def loadOriginalImage(self, filename, readFlag):
        """
        opencv incarca o poza \n
        :param filename: pathul catre fisier? \n
        :param readFlag: ??? \n
        :return: nimic \n
        """
        self.originalImage = opencv.imread(filename, readFlag)
