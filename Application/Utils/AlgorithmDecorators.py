from functools import wraps

from Application.ImageProcessingAlgorithms import registeredAlgorithms


class RegisterAlgorithm:

    def __init__(self, name, menuPath, before=None, fromMainModel=[], **kwargs):
        self._name = name
        self._menuPath = menuPath
        self._before = before
        self._fromMainModel = fromMainModel
        self._kwargs = kwargs

    def __call__(self, function):

        class AlgorithmWrapper:

            def __init__(self, func, name, menuPath, before=None, fromMainModel=[], **kwargs):
                self._func = func
                self._name = name
                self._menuPath = menuPath
                self._before = before
                self._fromMainModel = fromMainModel
                self.__dict__.update(kwargs)

                # functools.update_wrapper(self, func)

            @property
            def name(self):
                return self._name

            @property
            def menuPath(self):
                return self._menuPath

            @property
            def before(self):
                return self._before

            @wraps(function)
            def __call__(self, *args, **kwargs):
                return self._func(*args, **kwargs)

            def prepare(self, mainModel):
                return {argName: mainModel.__dict__[argName] for argName in self._fromMainModel}

        wrapper = AlgorithmWrapper(function, self._name, self._menuPath, self._before, self._fromMainModel, **self._kwargs)
        registeredAlgorithms[self._name] = wrapper
        return wrapper
