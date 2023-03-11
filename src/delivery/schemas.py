from pulsar.schema import *
import uuid
import time

def time_millis():
    return int(time.time() * 1000)

class EventoIntegracion(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()

class ProductSchema (Record):
    productReference = String()
    amount = Integer()

class WarehouseSchema (Record):
    origin = String()
    products = Array(ProductSchema())

class RoadMapSchema (Record):
    order_id = String()
    warehouses = Array(WarehouseSchema())

class ProductoPayload(Record):
    productReference = String()
    amount = Integer()

class LocationPayload(Record):
    address: String()

class WarehouseOrderPayload(Record):
    origin: LocationPayload()
    products: Array(ProductoPayload())

class CreatedOutboundPayload(Record):
    order_id: String()
    warehouses: Array(WarehouseOrderPayload())
    destination: String()

class CreatedOutboundEvent(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = CreatedOutboundPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
