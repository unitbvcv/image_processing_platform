from dataclasses import dataclass

from Application.Models.PlottingDataItemModel import PlottingDataItemModel


@dataclass(frozen=True)
class PlottingFunctionModel:
    """
    TODO: document PlotterWindowModel
    """

    originalImagePlotDataItems: PlottingDataItemModel = PlottingDataItemModel()
    processedImagePlotDataItems: PlottingDataItemModel = PlottingDataItemModel()
