from Application.Utils.AlgorithmDecorators import RegisterAlgorithm
from Application.Utils.InputDecorators import InputDialog
from Application.Utils.OutputDecorators import OutputDialog


@RegisterAlgorithm("Binarization", "Thresholding")
@InputDialog(threshold=int)
@OutputDialog(title="Binarization Output")
def binarization(image, threshold):
    """Applies binarization based on given threshold.

    :param image:
    :param threshold:
    :return:
    """
    # if the image is grayscale
    if len(image.shape) == 2:
        image[image < threshold] = 0
        image[image >= threshold] = 255
        return {
            'processedImage': image
        }
    else:
        return {
            'outputMessage': "Error: image is not grayscale!"
        }
