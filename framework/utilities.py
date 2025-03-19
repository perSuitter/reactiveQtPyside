
from functools import wraps
import importlib
import inspect
import os
import sys
import sys

from termcolor import colored


def nameFunctionDecorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        txt = "Calling Function: '" + func.__name__ + "' from Class '" + self.__class__.__name__ +"'" 
        txt = colored(txt, 'light_yellow')
        print(txt)
        result = func( self, *args, **kwargs)
        finalTxt = "End Function: '" + func.__name__ + "' from Class '" + self.__class__.__name__ + "'"+", Result: '" + str(result)
        finalTxt = colored(finalTxt, 'light_yellow')
        print(finalTxt)
        return result
    return wrapper

def decorateModelClasses(target):

    clsmembers = inspect.getmembers(target, inspect.isclass)

    for _, clsTarget in clsmembers:
        clsMethods = inspect.getmembers(clsTarget, predicate=inspect.isfunction)

        for clsMethodName,clsMethod in clsMethods:

            if clsMethodName.startswith("__") and clsMethodName.endswith("__"):
                continue

            setattr(clsTarget, clsMethodName,nameFunctionDecorator(clsMethod)) 


def prepareProject():
    VIEWS_PATH = "views"
    MODELS_PATH = "models"
    sys.path.append('./')
    import views
    import models
    pathList = [
        VIEWS_PATH,
        MODELS_PATH
    ]
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    for pathItem in pathList:
        sys.path.append(pathItem)
        decorateClasses(pathItem)

def decorateClasses( _path: str):
    #sys.path.append(_path)

    _pathModule = sys.modules[f"{_path}"].__path__[0]
    for root, dirs, files in os.walk(_pathModule):

        for targetFile in files:
            if targetFile.endswith(".py"):

                filePath = os.path.join(_pathModule, targetFile)

                spec1 = importlib.util.spec_from_file_location(f"{_path.replace('/','.')}.{targetFile.split('.')[0]}",filePath)

                foo1 = importlib.util.module_from_spec(spec1)
                sys.modules[f"{_path.replace('/','.')}.{targetFile.split('.')[0]}"] = foo1
                spec1.loader.exec_module(foo1)
                decorateModelClasses(foo1)
        break
