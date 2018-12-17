from Application.Utils.SmartDialog import SmartDialog


class InputDialog(object):

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __call__(self, func):

        class InputDialogWrapper:

            def __init__(self, func, requestedInputs):
                self._func = func
                self._requestedInputs = requestedInputs

            def __call__(self, *args, **kwargs):

                dialog = SmartDialog()
                readData = dialog.showDialog(**self._requestedInputs)

                return self._func(*args, **kwargs, **readData)

        return InputDialogWrapper(func, self._kwargs)
