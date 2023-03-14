from abc import ABC, abstractmethod
from warehouse_ms.seedwork.domain.entities import Entity
from warehouse_ms.seedwork.domain.repositories import Repository
from uuid import UUID

class WarehousesRepository(Repository, ABC):
    ...

class WarehouseProductsRepository(Repository, ABC):
    ...

class OutboundsRepository(Repository, ABC):
    ...
    @abstractmethod
    def find_by_order_id(self, order_id: UUID) -> Entity:
        ...

class OutboundsEventsRepository(Repository, ABC):
    ...

class ProductsRepository(Repository, ABC):
    ...
    @abstractmethod
    def find_by_outbound_id(self, outbound_id: UUID) -> list[Entity]:
        ...