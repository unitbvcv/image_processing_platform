import functools


class BaseWrapper:

    def __init__(self, func):
        self.hasResult = None
        self.result = None
        self.registeredAlgorithms = None
        self._func = func

        self._findRegisteredAlgorithms()

        functools.update_wrapper(self, self._func, functools.WRAPPER_ASSIGNMENTS + ('__bases__,',))

    # need to set members of BaseWrappers somehow
    # simply accessing them will create attributes in the wrapper
    def setResult(self, value):
        self.result = value

    def setHasResult(self, value):
        self.hasResult = value

    def __call__(self, *args, **kwargs):
        self.result = self._func(*args, **kwargs)
        self.hasResult = True
        return self.result

    def __getattr__(self, item):
        return getattr(self._func, item)

    def _findRegisteredAlgorithms(self):
        func_module_path = self._func.__module__.split('.')

        if 'ImageProcessingAlgorithms' in func_module_path:
            from Application.ImageProcessingAlgorithms import registeredAlgorithms
        elif 'PlottingAlgorithms' in func_module_path:
            from Application.PlottingAlgorithms import registeredAlgorithms

        self.registeredAlgorithms = registeredAlgorithms
