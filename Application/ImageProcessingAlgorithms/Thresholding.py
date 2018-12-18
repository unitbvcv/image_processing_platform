from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog


@RegisterAlgorithm("Binarization", "Thresholding")
@InputDialog(threshold=int)
@OutputDialog(title="Binarization Output")
def binarization(image, threshold):
    # if the image is grayscale
    if len(image.shape) == 2:
        image[image < threshold] = 0
        image[image >= threshold] = 255
        return image
    else:
        return None, "Error: image is not grayscale!"
