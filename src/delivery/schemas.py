from pulsar.schema import *

class ProductSchema (Record):
    productReference = String()
    amount = Integer()

class WarehouseSchema (Record):
    origin = String()
    products = Array(ProductSchema())

class RoadMapSchema (Record):
    orderId = String()
    warehouses = Array(WarehouseSchema())
