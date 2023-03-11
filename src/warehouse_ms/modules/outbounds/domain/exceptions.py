from warehouse_ms.seedwork.domain.exceptions import FactoryException

class ObjectTypeDoesNotExistsInOutboundsDomainException(FactoryException):
    def __init__(self, message='There is no factory for the requested type in the outbound module.'):
        self.__message = message
    def __str__(self):
        return str(self.__message)