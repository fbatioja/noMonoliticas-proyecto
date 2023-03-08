from abc import ABC
from warehouse_ms.seedwork.domain.repositories import Repository

class WarehousesRepository(Repository, ABC):
    ...

class WarehouseProductsRepository(Repository, ABC):
    ...

class OutboundsRepository(Repository, ABC):
    ...

class OutboundsEventsRepository(Repository, ABC):
    ...