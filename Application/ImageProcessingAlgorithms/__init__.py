import pkgutil


registeredAlgorithms = {}

for _importer, _modname, _is_pkg in pkgutil.iter_modules(__path__):
    if _modname[0] != '_':
        _fullModuleName = __package__ + '.' + _modname
        __import__(_fullModuleName)
