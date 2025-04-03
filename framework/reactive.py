from functools import wraps
import inspect
import types
from typing import Union
from .types import Model, View
from termcolor import colored

def reactivityConfigurationPrint(*txt:str):
    final = []
    for tt in txt:
        nt = colored(tt, 'magenta')

        final.append(nt)
    return final

def broadcastWrapper(destinations):
   
    def wrapss(func = None):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(*reactivityConfigurationPrint("View Destinations", destinations))
           
            for destination in destinations:
                result = None

                if callable(destination):
                    print(*reactivityConfigurationPrint("Destination is a function, executing"))
                    destination( *args, **kwargs)
                    continue
                if isinstance(destination, (tuple)) and len(destination) == 2 and callable(destination[1]):
                    print(*reactivityConfigurationPrint("Destination is a tuple"))
                    bridgeMethod = destination[1]
                    destination = destination[0]

                    print(*reactivityConfigurationPrint("Execute BridgeMethod"))
                    result =  bridgeMethod(*args, **kwargs)

                    print(*reactivityConfigurationPrint(f"Result from BridgeMethod {bridgeMethod.__name__} ", result))

                methods_callbacks = inspect.getmembers(destination, predicate=inspect.ismethod)
                allowedMethods = False
                for method in methods_callbacks:
                    if method[0] == 'render':
                        allowedMethods= True
                        print(*reactivityConfigurationPrint("Execute render with BridgeMethod result"))
                        getattr(destination, method[0])(result)

                    elif method[0] == 'set':
                        allowedMethods = True
                        print(*reactivityConfigurationPrint("Execute set with BridgeMethod result"))
                        getattr(destination, method[0])(result)
                if not allowedMethods:
                    raise Exception(f"Destination {destination} must have render or set methods")
        return wrapper
    
    return wrapss

def broadcastWrapperModel(destinations = None):
    print(*reactivityConfigurationPrint("broadcastWrapperModel"))
    def wrapss(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(*reactivityConfigurationPrint("Destinations",destinations))

            result =  func(*args, **kwargs)
            print(*reactivityConfigurationPrint(f"Result from {func.__name__}", result))


            for destination in destinations:

                if callable(destination):
                    print(*reactivityConfigurationPrint("Destination is a function, executing"))
                    destination(result, *args, **kwargs)
                    continue
                if isinstance(destination, (tuple)) and len(destination) == 2 and callable(destination[1]):
                    print(*reactivityConfigurationPrint("Destination is a tuple"))
                    bridgeMethod = destination[1]
                    destination = destination[0]

                    print(*reactivityConfigurationPrint("Execute BridgeMethod"))
                    result =  bridgeMethod(result, *args, **kwargs)

                    print(*reactivityConfigurationPrint(f"Result from BridgeMethod {bridgeMethod.__name__} ", result))

                methods_callbacks = inspect.getmembers(destination, predicate=inspect.ismethod)

                for method in methods_callbacks:
                    if method[0] == 'render':
                        print(*reactivityConfigurationPrint("Execute render with BridgeMethod result"))
                        getattr(destination, method[0])(result)

                    elif method[0] == 'set':
                        print(*reactivityConfigurationPrint("Execute set with BridgeMethod result"))
                        getattr(destination, method[0])(result)
            return result
        return wrapper
    
    return wrapss



def reactiveModelBridge(classPresenter):
    print(*reactivityConfigurationPrint("Creating reactiveModelBridge"))
    __init = classPresenter.__init__

    def __init__(self, origin, destinations: Model | View, *args, **kws):

        self.origin = origin

        __init(self, origin, destinations, *args, **kws) #
        model_methods = inspect.getmembers(origin, predicate=inspect.ismethod)

        set_method = next((method for method in model_methods if method[0] == 'set'), None)
        if not set_method:
            raise Exception(f"The model class {origin.__name__} has no method with set name")
        
        set_method_name , set_method = set_method

        get_method = next((method for method in model_methods if method[0] == 'get'), None)
        if not get_method:
            raise Exception(f"The model class {origin.__name__} has no method with get name")
        _ , get_method = get_method


        setattr(classPresenter, 'synchronize', broadcastWrapperModel(destinations)(get_method))

        def attachDestinations(self, *args, **kwargs):
            print(*reactivityConfigurationPrint("attachDestinations"))
            set_method(*args, **kwargs)
            classPresenter.synchronize()

        setAndSync = types.MethodType(attachDestinations, origin)

        print(*reactivityConfigurationPrint("Mutating set method of origin", origin))
        setattr(origin, set_method_name, setAndSync)
        
        print(*reactivityConfigurationPrint("call Presenter 'synchronize"))
        classPresenter.synchronize()


    classPresenter.__init__ = __init__ 
    return classPresenter
    
def reactiveViewBridge(classPresenter):
    print(*reactivityConfigurationPrint("Creating reactiveViewBridge"))
    __init = classPresenter.__init__

    def connnectEvent(event_name: str, origin, destinations):

        emitterMethod = broadcastWrapper(destinations)(None)

        print(*reactivityConfigurationPrint("emitterMethod", emitterMethod))
        print(*reactivityConfigurationPrint("connect event", event_name, f"from {origin.__class__.__name__} to {classPresenter.__name__} {emitterMethod.__name__}"))
        getattr(origin, event_name).connect(emitterMethod)

    def __init__(self, origin, destinations, events,  *args, **kws):
        self.origin = origin
        self.destinations = destinations
        #inspect methods
        __init(self, origin, destinations, events, *args, **kws) #

        for ev in events:

            connnectEvent(ev, origin, destinations)
  
    classPresenter.__init__ = __init__ 
    
    return classPresenter


class ViewBridge:
    def __init__(self, origin: View | Model, destinations: list[ Union[View ,Model , callable]], events: list[str], *args, **kws):
        pass

    def __new__(cls, origin: View | Model, destinations: list[ Union[View ,Model , callable]], events: list[str], *args, **kws):
        newClass = PresenterClassesGenerator(f"GenericViewBridge{origin.__class__.__name__}{generate()}", "view").get()
        newClass = reactiveViewBridge(newClass)
        return newClass( origin, destinations,events,  *args, **kws)
class ModelBridge:
    def __init__(self, origin: View | Model, destinations:  list[ Union[View ,Model , callable]], *args, **kws):
        pass

    def __new__(cls,  origin: View | Model, destinations:  list[ Union[View ,Model , callable]], *args, **kws):
        newClass = PresenterClassesGenerator(f"GenericModelBridge{origin.__class__.__name__}{generate()}", "model").get()
        newClass = reactiveModelBridge(newClass)
        return newClass( origin, destinations, *args, **kws)

def idGenerator():
    id = 0
    def getId():
        nonlocal id
        id += 1
        return id
    return getId
generate = idGenerator()
class PresenterClassesGenerator:
    def __init__(self, nameClass, entityType, *args, **kws):
        self.args = args
        self.kws = kws
        if entityType == "view":
            def construct(self, origin, destinations, events, *args, **kws):
                pass
            _construct = construct
            newClass = type(nameClass, (object,), {'__init__': _construct})

        if entityType == "model":
            def construct(self, origin, destinations, *args, **kws):
                pass
            _construct = construct
            newClass = type(nameClass, (object,), {'__init__': _construct})

        self.newClass = newClass
    def get(self):
        return self.newClass