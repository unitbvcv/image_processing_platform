import functools

from PyQt5.QtWidgets import QMessageBox


class OutputDialog:

    def __init__(self, title):
        self._title = title

    def __call__(self, function):

        class OutputDialogWrapper:

            def __init__(self, func, title):
                self._func = func
                self._title = title

                functools.update_wrapper(self, func)

            def __call__(self, *args, **kwargs):
                result = self._func(*args, **kwargs)
                QMessageBox.about(None, self._title, result[-1])
                return result[:-1]

        return OutputDialogWrapper(function, self._title)
