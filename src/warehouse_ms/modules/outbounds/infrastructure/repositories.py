from warehouse_ms.config.db import db
from warehouse_ms.modules.outbounds.domain.repositories import WarehousesRepository, WarehouseProductsRepository, OutboundsEventsRepository, OutboundsRepository
from warehouse_ms.modules.outbounds.domain.entities import Warehouse, Product, Outbound
from warehouse_ms.modules.outbounds.domain.factories import OutboundEventFactory, OutboundFactory, WarehouseFactory, WarehouseProductFactory
from .dto import Outbound as OutboundDTO
from .dto import Warehouse as WarehouseDTO
from .dto import WarehouseProduct as WarehouseProductDTO
from .dto import OutboundEvents
from .mappers import OutboundEventsMapper, OutboundMapper, WarehouseMapper, WarehouseProductMapper
from uuid import UUID
from pulsar.schema import *

class WarehousesRepositorySQLAlchemy(WarehousesRepository):

    def __init__(self):
        self._factory: WarehouseFactory = WarehouseFactory()

    @property
    def factory(self):
        return self._factory

    def find_by_id(self, id: UUID) -> Warehouse:
        warehouse_dto = db.session.query(WarehouseDTO).filter_by(id=str(id)).one()
        return self.factory.create_object(warehouse_dto, WarehouseMapper())

    def find_all(self) -> list[Warehouse]:
        # TODO
        raise NotImplementedError

    def add(self, entity: Warehouse):
        # TODO
        raise NotImplementedError

    def update(self, entity: Warehouse):
        # TODO
        raise NotImplementedError

    def delete(self, entity_id: UUID):
        # TODO
        raise NotImplementedError


class WarehouseProductsRepositorySQLAlchemy(WarehouseProductsRepository):

    def __init__(self):
        self._factory: WarehouseProductFactory = WarehouseProductFactory()

    @property
    def factory(self):
        return self._factory

    def find_by_id(self, id: UUID) -> Product:
        product_dto = db.session.query(WarehouseProductDTO).filter_by(id=str(id)).one()
        return self.factory.create_object(product_dto, WarehouseProductMapper())

    def find_all(self) -> list[Product]:
        # TODO
        raise NotImplementedError

    def add(self, entity: Product):
        # TODO
        raise NotImplementedError

    def update(self, entity: Product):
        product_dto = db.session.query(WarehouseProductDTO).filter_by(id=str(entity.warehouse_product.reference.productReference)).one()
        product_dto.available = entity.available
        product_dto.reserved = entity.reserved
        db.session.commit()

    def delete(self, entity_id: UUID):
        # TODO
        raise NotImplementedError

class OutboundsEventsRepositorySQLAlchemy(OutboundsEventsRepository):

    def __init__(self):
        self._factory: OutboundEventFactory = OutboundEventFactory()

    @property
    def factory(self):
        return self._factory

    def find_by_id(self, id: UUID) -> Outbound:
        outbound_event_dto = db.session.query(OutboundEvents).filter_by(id=str(id)).one()
        return self.factory.create_object(outbound_event_dto, OutboundEventsMapper())

    def find_all(self) -> list[Outbound]:
        raise NotImplementedError

    def add(self, event):
        outbound_event = self.factory.create_object(event, OutboundEventsMapper())

        parser_payload = JsonSchema(outbound_event.data.__class__)
        json_str = parser_payload.encode(outbound_event.data)

        evento_dto = OutboundEvents()
        evento_dto.id = str(event.id)
        evento_dto.entity_id = str(event.entity_id)
        evento_dto.event_datetime = event.event_datetime
        evento_dto.version = str(outbound_event.specversion)
        evento_dto.event_type = event.__class__.__name__
        evento_dto.content_type = 'JSON'
        evento_dto.service_name = str(outbound_event.service_name)
        evento_dto.content = json_str

        db.session.add(evento_dto)

    def update(self, outbound_event: Outbound):
        raise NotImplementedError

    def delete(self, outbound_event_id: UUID):
        raise NotImplementedError

class OutboundsRepositorySQLAlchemy(OutboundsRepository):

    def __init__(self):
        self._factory: OutboundFactory = OutboundFactory()

    @property
    def factory(self):
        return self._factory

    def find_by_id(self, id: UUID) -> Outbound:
        outbound_dto = db.session.query(OutboundDTO).filter_by(id=str(id)).one()
        return self.factory.create_object(outbound_dto, OutboundMapper())

    def find_all(self) -> list[Outbound]:
        raise NotImplementedError

    def add(self, entity: Outbound):
        outbound_dto = self.factory.create_object(entity, OutboundMapper())

        db.session.add(outbound_dto)
        db.session.commit()

    def update(self, outbound: Outbound):
        raise NotImplementedError

    def delete(self, outbound_id: UUID):
        raise NotImplementedError