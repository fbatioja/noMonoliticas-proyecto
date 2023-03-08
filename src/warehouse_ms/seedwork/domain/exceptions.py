from .rules import BusinessRule

class DomainException(Exception):
    ...

class IdEntityIsImmutableException(DomainException):
    def __init__(self, mensaje='The identificator must be immutable'):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)

class BusinessRuleException(DomainException):
    def __init__(self, regla: BusinessRule):
        self.regla = regla

    def __str__(self):
        return str(self.regla)

class FactoryException(DomainException):
    def __init__(self, mensaje):
        self.__mensaje = mensaje
    def __str__(self):
        return str(self.__mensaje)