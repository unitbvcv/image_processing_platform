from dataclasses import dataclass, field
from typing import Dict

from pyqtgraph import PlotDataItem


@dataclass
class PlottingDataItemModel:
    """
    TODO: document PlotterWindowModel
    """

    isDirty: bool = True
    availablePlotDataItems: Dict[str, PlotDataItem] = field(default_factory=lambda: {})
    visiblePlotDataItems: Dict[str, PlotDataItem] = field(default_factory=lambda: {})
