from dataclasses import dataclass


@dataclass
class MainModel(object):
    originalImage = None
    processedImage = None
    clickPosition = None
