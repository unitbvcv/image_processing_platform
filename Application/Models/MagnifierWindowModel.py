import Application.Settings


class MagnifierWindowModel:
    """
    TODO: document MagnifierWindowModel
    """

    def __init__(self):
        """
        TODO: document MagnifierWindowModel constructor
        """

        #: type??: Represents the position where the user has clicked on the image
        self._clickPosition = None

        self._colorSpace = Application.Settings.MagnifierWindowSettings.ColorSpaces.RGB

    @property
    def clickPosition(self):
        """
        TODO: MagnifierWindowModel click position documentation
        """
        return self._clickPosition

    @clickPosition.setter
    def clickPosition(self, value):
        self._clickPosition = value

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
