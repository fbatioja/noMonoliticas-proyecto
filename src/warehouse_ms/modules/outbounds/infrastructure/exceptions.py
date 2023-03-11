from warehouse_ms.seedwork.domain.exceptions import FactoryException

class ImplementationDoesNotExistsForFactoryTypeException(FactoryException):
    def __init__(self, message='Implementation does not exists for given repository.'):
        self.__message = message
    def __str__(self):
        return str(self.__message)