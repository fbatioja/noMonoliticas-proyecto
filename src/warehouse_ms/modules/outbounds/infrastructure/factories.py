from dataclasses import dataclass
from warehouse_ms.seedwork.domain.factories import Factory
from warehouse_ms.seedwork.domain.repositories import Repository
from warehouse_ms.modules.outbounds.domain.repositories import OutboundsEventsRepository, OutboundsRepository, WarehouseProductsRepository, WarehousesRepository
from .repositories import OutboundsEventsRepositorySQLAlchemy, OutboundsRepositorySQLAlchemy, WarehouseProductsRepositorySQLAlchemy, WarehousesRepositorySQLAlchemy
from .exceptions import FactoryException

@dataclass
class RepositoryFactory(Factory):
    def create_object(self, obj: type, mapper: any = None) -> Repository:
        if obj == OutboundsEventsRepository:
            return OutboundsEventsRepositorySQLAlchemy()
        elif obj == OutboundsRepository:
            return OutboundsRepositorySQLAlchemy()
        elif obj == WarehouseProductsRepository:
            return WarehouseProductsRepositorySQLAlchemy()
        elif obj == WarehousesRepository:
            return WarehousesRepositorySQLAlchemy()
        else:
            raise FactoryException(f'Factory for object {obj} does not exists')