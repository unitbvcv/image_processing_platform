from dataclasses import dataclass, field

from Application.Models.PlottingDataItemModel import PlottingDataItemModel


@dataclass(frozen=True)
class PlottingFunctionModel:
    """
    TODO: document PlottingFunctionModel
    """

    originalImagePlotDataItems: PlottingDataItemModel = field(default_factory=lambda: PlottingDataItemModel())
    processedImagePlotDataItems: PlottingDataItemModel = field(default_factory=lambda: PlottingDataItemModel())
