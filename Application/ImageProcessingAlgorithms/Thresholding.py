from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog


@InputDialog(threshold=int)
@OutputDialog(title="Binarization Output")
@RegisterAlgorithm("Binarization", "Thresholding")
def binarization(image, threshold):
    # if the image is grayscale
    if len(image.shape) == 2:
        image[image < threshold] = 0
        image[image >= threshold] = 255
        return image
    else:
        return None, "Error: image is not grayscale!"
