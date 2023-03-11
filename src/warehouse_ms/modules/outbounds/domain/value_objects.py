from __future__ import annotations

from dataclasses import dataclass, field
from warehouse_ms.seedwork.domain.value_objects import ValueObject
import uuid

@dataclass(frozen=True)
class Location(ValueObject):
    address: str
    
@dataclass(frozen=True)
class Reference(ValueObject):
    productReference: str
    
@dataclass(frozen=True)
class Amount(ValueObject):
    amount: int

@dataclass(frozen=True)
class OutboundProduct(ValueObject):
    productReference: Reference
    amount: Amount

@dataclass(frozen=True)
class WarehouseProduct(ValueObject):
    reference: Reference

@dataclass(frozen=True)
class WarehouseProductPair(ValueObject):
    warehouse_id: uuid.UUID
    origin: Location
    product: OutboundProduct

@dataclass(frozen=True)
class WarehouseOrder(ValueObject):
    origin: Location
    products: list[OutboundProduct] = field(default_factory=list[OutboundProduct])

    @classmethod
    def has_products(self) -> bool:
        return len(self.products) > 0

@dataclass(frozen=True)
class ProductOrder(ValueObject):
    products: list[OutboundProduct] = field(default_factory=list[OutboundProduct])

    @classmethod
    def has_products(self) -> bool:
        return len(self.products) > 0