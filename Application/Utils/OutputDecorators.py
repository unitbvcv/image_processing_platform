from functools import wraps

from PyQt5.QtWidgets import QMessageBox

from Application.ImageProcessingAlgorithms import registeredAlgorithms
from Application.Utils._BaseWrapper import BaseWrapper


class OutputDialog:

    def __init__(self, title="Output dialog"):
        self._title = title

    def __call__(self, function):

        # this checks if the function parameter contains in it a BaseWrapper (because function can be another wrapper)
        # can be checked for any other attribute of BaseWrapper
        # this is done to allow other decorators on the function
        # the downside is that a false positive may occur if any of the wrappers has an attribute with the same name
        if not hasattr(function, 'result'):
            function = BaseWrapper(function)

        class OutputDialogWrapper:

            def __init__(self, func, title):
                self._func = func
                self._title = title

                # functools.update_wrapper(self, func)

            def __getattr__(self, item):
                return getattr(self._func, item)

            @wraps(function)
            def __call__(self, *args, **kwargs):
                self._func(*args, **kwargs)
                if self._func.hasResult:
                    if isinstance(self._func.result, str):
                        QMessageBox.about(None, self._title, self._func.result)
                        self._func.setHasResult(False)
                        self._func.setResult(None)
                    else:
                        try:
                            if isinstance(self._func.result[-1], str):
                                QMessageBox.about(None, self._title, self._func.result[-1])
                                self._func.setResult(self._func.result[:-1])
                                if len(self._func.result) == 1:
                                    self._func.setResult(self._func.result[0])
                        except IndexError:
                            pass
                return self._func.result

        wrapper = OutputDialogWrapper(function, self._title)
        try:
            registeredAlgorithms[wrapper.name] = wrapper
        except AttributeError:
            for registeredFunctionName, registeredFunction in registeredAlgorithms.items():
                if function is registeredFunction:
                    registeredAlgorithms[registeredFunctionName] = wrapper
        return wrapper
