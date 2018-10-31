from dataclasses import dataclass, field
from typing import *


@dataclass(frozen=True)
class PlottingData:
    """
    TODO: document PlottingData

    Mention that it can be expanded and how.
    :return:
    """

    y: Iterable  # list, tuple, dictview, ndarray, set etc.
    x: Optional[Iterable] = None
    pen: Union[str, Tuple[int, int, int, int]] = 'w'
    name: Optional[str] = None
