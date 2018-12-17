from functools import wraps

from Application.Utils.SmartDialog import SmartDialog


class InputDialog:

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __call__(self, function):

        class InputDialogWrapper:

            def __init__(self, func, requestedInputs):
                self._func = func
                self._requestedInputs = requestedInputs

                # functools.update_wrapper(self, func)

            @wraps(function)
            def __call__(self, *args, **kwargs):

                dialog = SmartDialog()
                readData = dialog.showDialog(**self._requestedInputs)

                return self._func(*args, **kwargs, **readData)

        return InputDialogWrapper(function, self._kwargs)
