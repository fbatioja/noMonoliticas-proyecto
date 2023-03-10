from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from warehouse_ms.seedwork.domain.events import (DomainEvent)
import warehouse_ms.modules.outbounds.domain.value_objects as vo
import uuid
from datetime import datetime

class OutboundEvent(DomainEvent):
    ...

@dataclass
class OrderCreated(OutboundEvent):
    order_id: uuid.UUID = None
    products: vo.ProductOrder = None
    destination: vo.Location = None
    created_date: Optional[datetime] = None
    
@dataclass
class OrderCanceled(OutboundEvent):
    order_id: uuid.UUID = None
    products: vo.ProductOrder = None
    destination: vo.Location = None
    modification_date: Optional[datetime] = datetime.now()

@dataclass
class OutboundCreated(OutboundEvent):
    order_id: uuid.UUID = None
    warehouses: list[vo.WarehouseOrder] = None
    destination: vo.Location = None
    created_date: Optional[datetime] = None

@dataclass
class OutboundCanceled(OutboundEvent):
    order_id: uuid.UUID = None
    warehouses: vo.WarehouseOrder = None
    destination: vo.Location = None
    modification_date: Optional[datetime] = None