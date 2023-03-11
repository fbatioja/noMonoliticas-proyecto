from functools import singledispatch
from abc import ABC, abstractmethod

class Projection(ABC):
    @abstractmethod
    def execute(self):
        ...

class ProjectionHandler(ABC):
    @abstractmethod
    def handle(self, projection: Projection):
        ...

@singledispatch
def execute_projection(projection):
    raise NotImplementedError(f'Implementation for projection of type {type(projection).__name__} does not exists')