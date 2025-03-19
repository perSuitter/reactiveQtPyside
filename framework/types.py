from typing import Protocol



class Model(Protocol):
    def __init__(self):
        ...

    def set(self):
        ...

    def get(self, new):
        ...


class View(Protocol):
    def render(self):
        ...