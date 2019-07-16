import numpy

from Application.Models.PlottingData import PlottingData
from Application.Utils.PlotterDecorators import PlotterFunction
# from Application.Utils.InputDecorators import InputDialog
# from Application.Utils.OutputDecorators import OutputDialog


@PlotterFunction(name="Plot row values", fromMainModel=["leftClickPosition"], computeOnClick=True)
def plotRowValues(image, leftClickPosition):
    # TODO: take note that the function parameter must be named the same as the
    # fromMainModel parameters
    """
    TODO: document plotRowValues
    :param image:
    :param leftClickPosition:
    :return:
    """
    plotDataItemsList = []

    if image is None or leftClickPosition is None:
        return []

    # Grayscale image
    imageShapeLen = len(image.shape)
    if imageShapeLen == 2:
        plotName = 'Gray level'
        plottingData = PlottingData(plotName, image[leftClickPosition.y()], pen='r')
        plotDataItemsList.append(plottingData)

    # Color image
    elif imageShapeLen == 3:
        plotName = 'Red channel'
        plottingData = PlottingData(plotName, image[leftClickPosition.y(), :, 0], pen='r')
        plotDataItemsList.append(plottingData)

        plotName = 'Green channel'
        plottingData = PlottingData(plotName, image[leftClickPosition.y(), :, 1], pen='g')
        plotDataItemsList.append(plottingData)

        plotName = 'Blue channel'
        plottingData = PlottingData(plotName, image[leftClickPosition.y(), :, 2], pen='b')
        plotDataItemsList.append(plottingData)

    return plotDataItemsList


@PlotterFunction(name="Plot column values", fromMainModel=["leftClickPosition"], computeOnClick=True)
def plotColumnValues(image, leftClickPosition):
    # TODO: take note that the function parameter must be named the same as the
    # fromMainModel parameters
    """
    TODO: document plotColumnValues
    :param image:
    :param leftClickPosition:
    :return:
    """
    plotDataItemsList = []

    if image is None or leftClickPosition is None:
        return []

    # Grayscale image
    imageShapeLen = len(image.shape)
    if imageShapeLen == 2:
        plotName = 'Gray level'
        plottingData = PlottingData(plotName, image[:, leftClickPosition.x()], pen='r')
        plotDataItemsList.append(plottingData)

    # Color image
    elif imageShapeLen == 3:
        plotName = 'Red channel'
        plottingData = PlottingData(plotName, image[:, leftClickPosition.x(), 0], pen='r')
        plotDataItemsList.append(plottingData)

        plotName = 'Green channel'
        plottingData = PlottingData(plotName, image[:, leftClickPosition.y(), 1], pen='g')
        plotDataItemsList.append(plottingData)

        plotName = 'Blue channel'
        plottingData = PlottingData(plotName, image[:, leftClickPosition.y(), 2], pen='b')
        plotDataItemsList.append(plottingData)

    return plotDataItemsList


@PlotterFunction(name="Plot histogram", computeOnImageChanged=True)
def plotHistogram(image):
    """
    TODO: document plotHistogram
    :param image:
    :return:
    """
    plotDataItemsList = []

    if image is None:
        return []

    imageShapeLen = len(image.shape)

    # Grayscale image
    if imageShapeLen == 2:
        # numpy.histogram returns the histogram first and the buckets second
        # the last bin is shared between the last two elements, so we need one more
        # range(256) gives us [0, ..., 255], so we need range(257)
        # the first element in the range parameter needs to be lower than the first needed element
        histogram = numpy.histogram(image, bins=range(257), range=(-1, 255))[0]
        plotName = 'Gray histogram'
        plottingData = PlottingData(plotName, histogram, pen='r')
        plotDataItemsList.append(plottingData)

    # Color image
    elif imageShapeLen == 3:
        histogram = numpy.histogram(image[:, :, 0], bins=range(257), range=(-1, 255))[0]
        plotName = 'Red histogram'
        plottingData = PlottingData(plotName, histogram, pen='r')
        plotDataItemsList.append(plottingData)

        histogram = numpy.histogram(image[:, :, 1], bins=range(257), range=(-1, 255))[0]
        plotName = 'Green histogram'
        plottingData = PlottingData(plotName, histogram, pen='g')
        plotDataItemsList.append(plottingData)

        histogram = numpy.histogram(image[:, :, 2], bins=range(257), range=(-1, 255))[0]
        plotName = 'Blue histogram'
        plottingData = PlottingData(plotName, histogram, pen='b')
        plotDataItemsList.append(plottingData)

    return plotDataItemsList
