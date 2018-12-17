import numpy

from Application.Utils.AlgorithmDecorators import RegisterAlgorithm


@RegisterAlgorithm("Invert", "PointwiseOp")
def invert(image):
    return numpy.invert(image)
