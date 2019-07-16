import functools

from Application.Utils._BaseWrapper import BaseWrapper


class PlotterFunction:

    def __init__(self, name, fromMainModel=[], computeOnImageChanged=False, computeOnClick=False, **kwargs):
        self._name = name
        self._fromMainModel = fromMainModel
        self._computeOnImageChanged = computeOnImageChanged
        self._computeOnClick = computeOnClick
        self._kwargs = kwargs

    def __call__(self, function):

        class PlotterFunctionWrapper:
            def __init__(self, name, func, argList, onChange, onClick, **kwargs):
                self._name = name
                self._argNames = argList
                self._func = func
                self._computeOnImageChanged = onChange
                self._computeOnClick = onClick
                self.__dict__.update(kwargs)

                functools.update_wrapper(self, self._func, functools.WRAPPER_ASSIGNMENTS + ('__bases__,',), [])

            def __getattr__(self, item):
                return getattr(self._func, item)

            @property
            def name(self):
                return self._name

            @property
            def computeOnImageChanged(self):
                return self._computeOnImageChanged

            @property
            def computeOnClick(self):
                return self._computeOnClick

            def __call__(self, *args, **kwargs):
                self._func(*args, **kwargs)
                try:
                    if self._func.result is None or len(self._func.result) == 0:
                        self._func.setHasResult(False)
                        self._func.setResult(None)
                except TypeError:
                    pass
                return self._func.result

            def prepare(self, mainModel):
                return {argName: mainModel.__dict__[argName] for argName in self._argNames}

        if not hasattr(function, 'result'):
            function = BaseWrapper(function)

        wrapper = PlotterFunctionWrapper(
            self._name,
            function,
            self._fromMainModel,
            self._computeOnImageChanged,
            self._computeOnClick,
            **self._kwargs
        )
        function.registeredAlgorithms[self._name] = wrapper
        return wrapper
