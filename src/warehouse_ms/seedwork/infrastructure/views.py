from abc import ABC, abstractmethod

class View(ABC):

    @abstractmethod
    def find_by(**kwargs):
        ...