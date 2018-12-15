from dataclasses import dataclass, field
from typing import Dict

from pyqtgraph import PlotDataItem


@dataclass
class PlottingDataItemModel:
    """
    TODO: document PlottingDataItemModel
    """

    isDirty: bool = True
    availablePlotDataItems: Dict[str, PlotDataItem] = field(default_factory=lambda: {})
    visiblePlotDataItems: Dict[str, PlotDataItem] = field(default_factory=lambda: {})

    def clear(self):
        self.availablePlotDataItems.clear()
        self.visiblePlotDataItems.clear()
        self.isDirty = True  # trebuie si asta
