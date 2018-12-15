import numpy

from Application.Models.PlottingData import PlottingData
from Application.PlottingAlgorithms._PlotterDecorators import PlotterFunction


@PlotterFunction(title="Plot row values", fromMainModel=["clickPosition"], computeOnClick=True)
def plotRowValues(image, clickPosition):
    """
    TODO: document plotRowValues
    :param image:
    :param clickPosition:
    :return:
    """
    plotDataItemsList = []

    if image is None:
        # TODO: what happens in this case ?
        return None  # sau [] sau throw exception ?

    # Grayscale image
    if len(image.shape) == 2:
        plotName = 'Gray level'
        plottingData = PlottingData(plotName, image[clickPosition.y()], pen='r')
        plotDataItemsList.append(plottingData)

    # Color image
    elif len(image.shape) == 3:
        plotName = 'Red channel'
        plottingData = PlottingData(plotName, image[clickPosition.y(), :, 2], pen='r')
        plotDataItemsList.append(plottingData)

        plotName = 'Green channel'
        plottingData = PlottingData(plotName, image[clickPosition.y(), :, 1], pen='g')
        plotDataItemsList.append(plottingData)

        plotName = 'Blue channel'
        plottingData = PlottingData(plotName, image[clickPosition.y(), :, 0], pen='b')
        plotDataItemsList.append(plottingData)

    return plotDataItemsList


@PlotterFunction(title="Plot column values", fromMainModel=["clickPosition"], computeOnClick=True)
def plotColumnValues(image, clickPosition):
    """
    TODO: document plotColumnValues
    :param image:
    :param clickPosition:
    :return:
    """
    plotDataItemsList = []

    if image is None:
        # TODO: what happens in this case ?
        return None  # sau [] sau throw exception ?

    # Grayscale image
    if len(image.shape) == 2:
        plotName = 'Gray level'
        plottingData = PlottingData(plotName, image[:, clickPosition.x()], pen='r')
        plotDataItemsList.append(plottingData)

    # Color image
    elif len(image.shape) == 3:
        plotName = 'Red channel'
        plottingData = PlottingData(plotName, image[:, clickPosition.x(), 2], pen='r')
        plotDataItemsList.append(plottingData)

        plotName = 'Green channel'
        plottingData = PlottingData(plotName, image[:, clickPosition.y(), 1], pen='g')
        plotDataItemsList.append(plottingData)

        plotName = 'Blue channel'
        plottingData = PlottingData(plotName, image[:, clickPosition.y(), 0], pen='b')
        plotDataItemsList.append(plottingData)

    return plotDataItemsList


@PlotterFunction(title="Plot histogram", computeOnImageChanged=True)
def plotHistogram(image):
    """
    TODO: document plotHistogram
    :param image:
    :return:
    """
    plotDataItemsList = []

    if image is None:
        # TODO: what happens in this case ?
        return None  # sau [] sau throw exception ?

    # Grayscale image
    if len(image.shape) == 2:
        # numpy.histogram returns the histogram first and the buckets second
        # the last bin is shared between the last two elements, so we need one more
        # range(256) gives us [0, ..., 255], so we need range(257)
        # the first element in the range parameter needs to be lower than the first needed element
        histogram = numpy.histogram(image, bins=range(257), range=(-1, 255))[0]
        plotName = 'Gray histogram'
        plottingData = PlottingData(plotName, histogram, pen='r')
        plotDataItemsList.append(plottingData)

    # Color image
    elif len(image.shape) == 3:
        histogram = numpy.histogram(image[:, :, 2], bins=range(257), range=(-1, 255))[0]
        plotName = 'Red histogram'
        plottingData = PlottingData(plotName, histogram, pen='r')
        plotDataItemsList.append(plottingData)

        histogram = numpy.histogram(image[:, :, 1], bins=range(257), range=(-1, 255))[0]
        plotName = 'Green histogram'
        plottingData = PlottingData(plotName, histogram, pen='g')
        plotDataItemsList.append(plottingData)

        histogram = numpy.histogram(image[:, :, 0], bins=range(257), range=(-1, 255))[0]
        plotName = 'Blue histogram'
        plottingData = PlottingData(plotName, histogram, pen='b')
        plotDataItemsList.append(plottingData)

    return plotDataItemsList
