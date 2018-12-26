import functools

from Application.ImageProcessingAlgorithms import registeredAlgorithms
from Application.Utils._BaseWrapper import BaseWrapper


class RegisterAlgorithm:

    def __init__(self, name, menuPath, before=None, fromMainModel=[], **kwargs):
        self._name = name
        self._menuPath = menuPath
        self._before = before
        self._fromMainModel = fromMainModel
        self._kwargs = kwargs

    def __call__(self, function):

        # this checks if the function parameter contains in it a BaseWrapper (because function can be another wrapper)
        # can be checked for any other attribute of BaseWrapper
        # this is done to allow other decorators on the function
        # the downside is that a false positive may occur if any of the wrappers has an attribute with the same name
        if not hasattr(function, 'result'):
            function = BaseWrapper(function)

        class AlgorithmWrapper:

            def __init__(self, func, name, menuPath, before=None, fromMainModel=[], **kwargs):
                self._func = func
                self._name = name
                self._menuPath = menuPath
                self._before = before
                self._fromMainModel = fromMainModel
                self.__dict__.update(kwargs)

                functools.update_wrapper(self, self._func, functools.WRAPPER_ASSIGNMENTS+('__bases__,',), [])

            def __getattr__(self, item):
                return getattr(self._func, item)

            @property
            def name(self):
                return self._name

            @property
            def menuPath(self):
                return self._menuPath

            @property
            def before(self):
                return self._before

            def __call__(self, *args, **kwargs):
                return self._func(*args, **kwargs)

            def prepare(self, mainModel):
                return {argName: getattr(mainModel, argName) for argName in self._fromMainModel}

        wrapper = AlgorithmWrapper(
            function,
            self._name,
            self._menuPath,
            self._before,
            self._fromMainModel,
            **self._kwargs
        )
        registeredAlgorithms[wrapper.name] = wrapper
        return wrapper
