from functools import wraps

from Application.PlottingAlgorithms import registeredAlgorithms


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

                # functools.update_wrapper(self, func)

            @property
            def name(self):
                return self._name

            @property
            def computeOnImageChanged(self):
                return self._computeOnImageChanged

            @property
            def computeOnClick(self):
                return self._computeOnClick

            @wraps(function)
            def __call__(self, *args, **kwargs):
                return self._func(*args, **kwargs)

            def prepare(self, mainModel):
                return {argName: mainModel.__dict__[argName] for argName in self._argNames}

        wrapper = PlotterFunctionWrapper(
            self._name,
            function,
            self._fromMainModel,
            self._computeOnImageChanged,
            self._computeOnClick,
            **self._kwargs
        )
        registeredAlgorithms[self._name] = wrapper
        return wrapper
