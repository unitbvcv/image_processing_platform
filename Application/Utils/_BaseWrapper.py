class BaseWrapper:  # dataclass?

    def __init__(self, func):
        self.hasResult = None
        self.result = None
        self._func = func

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
