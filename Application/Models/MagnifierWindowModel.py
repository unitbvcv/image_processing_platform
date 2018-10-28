import Application.Settings


class MagnifierWindowModel:
    """
    TODO: document MagnifierWindowModel
    """

    def __init__(self):
        """
        TODO: document MagnifierWindowModel constructor
        """
        self._colorSpace = Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB

    @property
    def colorSpace(self):
        """
        TODO: MagnifierWindowModel colorSpace documentation
        :return:
        """
        return self._colorSpace

    @colorSpace.setter
    def colorSpace(self, value):
        self._colorSpace = value
