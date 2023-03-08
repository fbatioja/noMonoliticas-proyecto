from __future__ import annotations
from dataclasses import dataclass, field
import datetime
import uuid

import warehouse_ms.modules.outbounds.domain.value_objects as vo
from warehouse_ms.modules.outbounds.domain.events import OrderCreated, OrderCanceled, OutboundCreated, OutboundCanceled
from warehouse_ms.seedwork.domain.entities import RootAggregation, Entity

@dataclass
class Warehouse(Entity):
    location: vo.Location = field(default_factory=vo.Location)

@dataclass
class Product(Entity):
    warehouse_product: vo.WarehouseProduct = field(default_factory=vo.WarehouseProduct)
    warehouse_id: uuid.UUID = field(hash=True, default=None)
    available: int = field(default=0)
    reserved: int = field(default=0)

    def order_stock(self, amount: int):
        self.available -= amount
        self.reserved += amount

    def cancel_stock(self, amount: int):
        self.available += amount
        self.reserved -= amount

@dataclass
class Outbound(RootAggregation):
    order_id: uuid.UUID = field(hash=True, default=None)
    product_order: vo.ProductOrder = field(default_factory=vo.ProductOrder)
    destination: vo.Location = field(default_factory=vo.Location)

    def create_outbound(self):
        self.created_date = datetime.datetime.now()

        self.add_event(OutboundCreated(self.id, self.modification_date, self.order_id, self.product_order, self.destination, self.created_date), 
                       OutboundCanceled(self.id, self.modification_date, self.order_id, self.product_order, self.destination, self.modification_date))

    def notify_outbound(self):
        self.modification_date = datetime.datetime.now()

        self.add_event(OutboundCreated(self.id, self.modification_date, self.order_id, self.product_order, self.destination, self.created_date), 
                       OutboundCanceled(self.id, self.modification_date, self.order_id, self.product_order, self.destination, self.modification_date))