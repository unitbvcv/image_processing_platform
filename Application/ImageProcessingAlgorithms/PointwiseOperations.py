"""
Module docstring?
"""
import numpy

from Application.Utils.AlgorithmDecorators import RegisterAlgorithm


@RegisterAlgorithm("Invert", "PointwiseOp")
def invert(image):
    """Inverts every pixel of the image.

    :param image:
    :return:
    """
    return numpy.invert(image)
