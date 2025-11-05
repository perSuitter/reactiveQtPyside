
from functools import wraps
import importlib
import inspect
import os
from pathlib import Path
import sys
import sys

from termcolor import colored

_LOGGING_COLOR = 'light_yellow'

def nameFunctionDecorator(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        txt = "Calling Function: '" + func.__name__ + "' from Class '" + self.__class__.__name__ +"'" 
        txt = colored(txt, _LOGGING_COLOR)
        print(txt)
        result = func( self, *args, **kwargs)
        finalTxt = "End Function: '" + func.__name__ + "' from Class '" + self.__class__.__name__ + "'"+", Result: '" + str(result)
        finalTxt = colored(finalTxt, _LOGGING_COLOR)
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

    import json

    config_path = Path.cwd().joinpath("framework/config.json")
    _exists = os.path.exists(config_path)

    if not _exists:
        print("config.json not found")
        return

    with open(config_path) as f:
        data = json.load(f)

    if "logging" not in data:
        print("No logging configuration found")
        return
    
    if not "paths" in data["logging"]:
        print("No logging paths found")
        return
    pathList = data["logging"]["paths"]
    for pathItem in pathList:
        if Path.cwd().joinpath(pathItem).exists():
            __import__(pathItem)
            decorateClasses(pathItem)

def decorateClasses( _path: str):


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
