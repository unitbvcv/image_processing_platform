from functools import wraps

from Application.Utils.SmartDialog import SmartDialog
from Application.ImageProcessingAlgorithms import registeredAlgorithms


class InputDialog:

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __call__(self, function):

        class InputDialogWrapper:

            def __init__(self, func, requestedInputs):
                self._func = func
                self._requestedInputs = requestedInputs

                # functools.update_wrapper(self, func)

            def __getattr__(self, item):
                return getattr(self._func, item)

            @wraps(function)
            def __call__(self, *args, **kwargs):

                dialog = SmartDialog()
                # readData = dialog.showDialog(**self._requestedInputs)
                # if readData is not None:
                #     return self._func(*args, **kwargs, **readData)
                dialog.showDialog(**self._requestedInputs)
                if dialog.cancelled is False:
                    return self._func(*args, **kwargs, **dialog.readData)

        wrapper = InputDialogWrapper(function, self._kwargs)
        for registeredFunctionName, registeredFunction in registeredAlgorithms.items():
            if function is registeredFunction:
                registeredAlgorithms[registeredFunctionName] = wrapper
        return wrapper
