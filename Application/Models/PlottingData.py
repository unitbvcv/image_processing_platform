from dataclasses import dataclass
from typing import Iterable, Optional, Union, Tuple

from pyqtgraph import PlotDataItem


@dataclass(frozen=True)
class PlottingData:
    """
    TODO: document PlottingData

    Mention that it can be expanded and how.
    :return:
    """

    name: str
    y: Iterable  # list, tuple, dictview, ndarray, set, generator etc.
    x: Optional[Iterable] = None
    pen: Union[str, Tuple[int, int, int, int]] = 'w'

    def toPlotDataItem(self):
        return PlotDataItem(x=self.x, y=self.y, pen=self.pen, name=self.name)
