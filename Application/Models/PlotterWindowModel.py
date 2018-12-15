from dataclasses import dataclass, field
from typing import Dict

from Application.Models.PlottingFunctionModel import PlottingFunctionModel


@dataclass(frozen=True)  # because the references to the dicts never change; remove if necessary
class PlotterWindowModel:
    """
    TODO: document PlotterWindowModel
    """

    functionModels: Dict[str, PlottingFunctionModel] = field(default_factory=lambda: {})
