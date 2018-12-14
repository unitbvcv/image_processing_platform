from dataclasses import dataclass, field
from typing import Dict

from Application.Models.PlottingFunctionModel import PlotingFunctionModel


@dataclass(frozen=True)  # because the references to the dicts never change; remove if necessary
class PlotterWindowModel:
    """
    TODO: document PlotterWindowModel
    """

    functionModels: Dict[str, PlotingFunctionModel] = field(default_factory=lambda: {})
    
    # availablePlotDataItemsOriginalImage: Dict[str, PlotDataItem] = field(default_factory=lambda: {})
    # availablePlotDataItemsProcessedImage: Dict[str, PlotDataItem] = field(default_factory=lambda: {})
    #
    # visiblePlotDataItemsOriginalImage: Dict[str, PlotDataItem] = field(default_factory=lambda: {})
    # visiblePlotDataItemsProcessedImage: Dict[str, PlotDataItem] = field(default_factory=lambda: {})