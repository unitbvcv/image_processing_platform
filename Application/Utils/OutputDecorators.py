from functools import wraps

from PyQt5.QtWidgets import QMessageBox

from Application.ImageProcessingAlgorithms import registeredAlgorithms


class OutputDialog:

    def __init__(self, title="Output dialog"):
        self._title = title

    def __call__(self, function):

        class OutputDialogWrapper:

            def __init__(self, func, title):
                self._func = func
                self._title = title

                # functools.update_wrapper(self, func)

            def __getattr__(self, item):
                return getattr(self._func, item)

            @wraps(function)
            def __call__(self, *args, **kwargs):
                result = self._func(*args, **kwargs)
                if isinstance(result, tuple):
                    QMessageBox.about(None, self._title, result[-1])
                    result = result[:-1]
                return result

        wrapper = OutputDialogWrapper(function, self._title)
        for registeredFunctionName, registeredFunction in registeredAlgorithms.items():
            if function is registeredFunction:
                registeredAlgorithms[registeredFunctionName] = wrapper
        return wrapper
