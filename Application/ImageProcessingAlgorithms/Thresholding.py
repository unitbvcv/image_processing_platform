import numpy

from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog


@RegisterAlgorithm("Binarization", "Thresholding")
@InputDialog(threshold=int)
def binarization(image, threshold):
    pass