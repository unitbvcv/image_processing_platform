class PlotterWindowModel:
    """
    TODO: document PlotterWindowModel
    """

    def __init__(self):
        """
        TODO: document PlotterWindowModel constructor
        :param self:
        :return:
        """
        self._availablePlotDataItemsOriginalImage = {}
        self._availablePlotDataItemsProcessedImage = {}

        self._visiblePlotDataItemsOriginalImage = {}
        self._visiblePlotDataItemsProcessedImage = {}

    @property
    def availablePlotDataItemsOriginalImage(self):
        """
        TODO: document PlotterWindowModel availablePlotDataItemsOriginalImage
        :return:
        """
        return self._availablePlotDataItemsOriginalImage

    @property
    def availablePlotDataItemsProcessedImage(self):
        """
        TODO: document PlotterWindowModel availablePlotDataItemsProcessedImage
        :return:
        """
        return self._availablePlotDataItemsProcessedImage()

    @property
    def visiblePlotDataItemsOriginalImage(self):
        """
        TODO: document PlotterWindowModel visiblePlotDataItemsOriginalImage
        :return:
        """
        return self._visiblePlotDataItemsOriginalImage

    @property
    def visiblePlotDataItemsProcessedImage(self):
        """
        TODO: document PlotterWindowModel visiblePlotDataItemsProcessedImage
        :return:
        """
        return self._visiblePlotDataItemsProcessedImage
