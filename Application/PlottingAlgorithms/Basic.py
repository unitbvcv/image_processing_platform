from Application.Models.PlottingData import PlottingData

@PlotterFunction(title="Plot row values", fromMainModel=["clickPosition"], always_recalculate=True)
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
        plottingData = PlottingData(image[clickPosition.y()], pen='r', name=plotName)
        plotDataItemsList.append(plottingData)

    # Original color image
    elif len(image.shape) == 3:
        plotName = 'Red channel'
        plottingData = PlottingData(image[clickPosition.y(), :, 2], pen='r', name=plotName)
        plotDataItemsList.append(plottingData)

        plotName = 'Green channel'
        plottingData = PlottingData(image[clickPosition.y(), :, 1], pen='g', name=plotName)
        plotDataItemsList.append(plottingData)

        plotName = 'Blue channel'
        plottingData = PlottingData(image[clickPosition.y(), :, 0], pen='b', name=plotName)
        plotDataItemsList.append(plottingData)

    return plotDataItemsList


@PlotterFunction(title="Plot column values", fromMainModel=["clickPosition"], always_recalculate=True)
def plotColumnValues(image, clickPosition):
    pass
