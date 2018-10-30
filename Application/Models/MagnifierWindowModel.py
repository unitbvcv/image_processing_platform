from dataclasses import dataclass, field
from Application.Settings import MagnifierWindowSettings


@dataclass
class MagnifierWindowModel:
    """
    TODO: document MagnifierWindowModel
    """

    colorSpace: MagnifierWindowSettings.ColorSpaces = field(default=MagnifierWindowSettings.ColorSpaces.RGB)
