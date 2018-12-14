import functools
from Application.PlottingAlgorithms import registeredAlgorithms


class PlotterFunction(object):

    def __init__(self, title, fromMainModel=[], computeOnImageChanged=False, computeOnClick=False, **kwargs):
        self._title = title
        self._fromMainModel = fromMainModel
        self._computeOnImageChanged = computeOnImageChanged
        self._computeOnClick = computeOnClick
        self.__dict__.update(kwargs)

    def __call__(self, func):

        class PlotterFunctionWrapper:
            def __init__(self, func, argList, onChange, onClick, **kwargs):
                self._argNames = argList
                self._func = func
                self._computeOnImageChanged = onChange
                self._computeOnClick = onClick
                self.__dict__.update(kwargs)

                functools.update_wrapper(self, func)

            @property
            def computeOnImageChanged(self):
                return self._computeOnImageChanged

            @property
            def computeOnClick(self):
                return self._computeOnClick

            def __call__(self, *args, **kwargs):
                return self._func(*args, **kwargs)

            def prepare(self, mainModel):
                return {argName: mainModel.__dict__[argName] for argName in self._argNames}

        wrapper = PlotterFunctionWrapper(func, self._fromMainModel, self._computeOnImageChanged, self._computeOnClick)
        registeredAlgorithms[self._title] = wrapper
        return wrapper
