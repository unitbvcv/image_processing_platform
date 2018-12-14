from dataclasses import dataclass, field
from typing import Dict

from pyqtgraph import PlotDataItem


@dataclass()  # because the references to the dicts never change; remove if necessary
class PlottingFunctionModel:
    """
    TODO: document PlotterWindowModel
    """

    isDirty: bool = True

    availablePlotDataItemsOriginalImage: Dict[str, PlotDataItem] = field(default_factory=lambda: {})
    availablePlotDataItemsProcessedImage: Dict[str, PlotDataItem] = field(default_factory=lambda: {})

    visiblePlotDataItemsOriginalImage: Dict[str, PlotDataItem] = field(default_factory=lambda: {})
    visiblePlotDataItemsProcessedImage: Dict[str, PlotDataItem] = field(default_factory=lambda: {})
