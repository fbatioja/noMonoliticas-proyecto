from .events import OutboundEvent
from .entities import Outbound, Product, Warehouse
from .rules import ValidAvailableStock, ValidReservedStock, ValidWarehouseOrder, ValidLocation
from .exceptions import ObjectTypeDoesNotExistsInOutboundsDomainException
from warehouse_ms.seedwork.domain.repositories import Mapper
from warehouse_ms.seedwork.domain.factories import Factory
from warehouse_ms.seedwork.domain.entities import Entity
from warehouse_ms.seedwork.domain.events import DomainEvent
from dataclasses import dataclass

@dataclass
class _OutboundFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)
        else:
            outbound: Outbound = mapper.dto_to_entity(obj)

            [self.validate_rule(ValidAvailableStock(product.stock)) for product in outbound.product_order.products]
            [self.validate_rule(ValidReservedStock(product.stock)) for product in outbound.product_order.products]
            self.validate_rule(ValidWarehouseOrder(outbound.product_order))
            
            return outbound

@dataclass
class _OutboundEventFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)
        else:
            raise ObjectTypeDoesNotExistsInOutboundsDomainException()

@dataclass
class _WarehouseProductFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)
        else:
            product: Product = mapper.dto_to_entity(obj)

            self.validate_rule(ValidAvailableStock(product.available))
            self.validate_rule(ValidReservedStock(product.reserved))
            
            return product

@dataclass
class _WarehouseFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if isinstance(obj, Entity) or isinstance(obj, DomainEvent):
            return mapper.entity_to_dto(obj)
        else:
            warehouse: Warehouse = mapper.dto_to_entity(obj)

            self.validate_rule(ValidLocation(warehouse.location))
            
            return warehouse

@dataclass
class OutboundFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if mapper.get_type() == Outbound.__class__:
            outbound_factory = _OutboundFactory()
            return outbound_factory.create_object(obj, mapper)
        else:
            raise ObjectTypeDoesNotExistsInOutboundsDomainException()

@dataclass
class OutboundEventFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if mapper.get_type() == OutboundEvent.__class__:
            outbound_event_factory = _OutboundEventFactory()
            return outbound_event_factory.create_object(obj, mapper)
        else:
            raise ObjectTypeDoesNotExistsInOutboundsDomainException()

@dataclass
class WarehouseProductFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if mapper.get_type() == Product.__class__:
            product_factory = _WarehouseProductFactory()
            return product_factory.create_object(obj, mapper)
        else:
            raise ObjectTypeDoesNotExistsInOutboundsDomainException()

@dataclass
class WarehouseFactory(Factory):
    def create_object(self, obj: any, mapper: Mapper) -> any:
        if mapper.get_type() == Warehouse.__class__:
            warehouse_factory = _WarehouseFactory()
            return warehouse_factory.create_object(obj, mapper)
        else:
            raise ObjectTypeDoesNotExistsInOutboundsDomainException()