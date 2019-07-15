import functools

from Application.Utils.SmartDialog import SmartDialog
from Application.Utils._BaseWrapper import BaseWrapper


class InputDialog:

    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def __call__(self, function):

        # this checks if the function parameter contains in it a BaseWrapper (because function can be another wrapper)
        # can be checked for any other attribute of BaseWrapper
        # this is done to allow other decorators on the function
        # the downside is that a false positive may occur if any of the wrappers has an attribute with the same name
        if not hasattr(function, 'result'):
            function = BaseWrapper(function)

        class InputDialogWrapper:

            def __init__(self, func, requestedInputs):
                self._func = func
                self._requestedInputs = requestedInputs

                functools.update_wrapper(self, self._func, functools.WRAPPER_ASSIGNMENTS + ('__bases__,',), [])

            def __getattr__(self, item):
                return getattr(self._func, item)

            def __call__(self, *args, **kwargs):

                dialog = SmartDialog()
                dialog.showDialog(**self._requestedInputs)
                if dialog.cancelled:
                    self._func.setHasResult(False)
                    return
                return self._func(*args, **kwargs, **dialog.readData)

        wrapper = InputDialogWrapper(function, self._kwargs)
        try:
            function.registeredAlgorithms[wrapper.name] = wrapper
        except AttributeError:
            for registeredFunctionName, registeredFunction in function.registeredAlgorithms.items():
                if function is registeredFunction:
                    function.registeredAlgorithms[registeredFunctionName] = wrapper
        return wrapper
