import pkgutil, os, importlib

for i, mod in enumerate(pkgutil.iter_modules([os.path.dirname(__file__)])):
    importlib.import_module(__name__ + '.' + mod.name)
