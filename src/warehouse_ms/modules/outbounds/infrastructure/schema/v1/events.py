from pulsar.schema import *
import warehouse_ms.modules.outbounds.domain.value_objects as vo
from warehouse_ms.seedwork.infrastructure.schema.v1.events import IntegrationEvent
from warehouse_ms.seedwork.infrastructure.utils import time_millis
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

class ProductoPayload(Record):
    productReference = String()
    amount = Integer()

class OrdenCreadaPayload(Record):
    destiny = String()
    products =Array(ProductoPayload())

class EventoOrdenCreada(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = OrdenCreadaPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class LocationPayload(Record):
    address: String()

class ReferencePayload(Record):
    reference: String()

class AmountPayload(Record):
    amount: Integer()

class OutboundProductPayload(Record):
    productReference: String()
    amount: Integer()

class WarehouseOrderPayload(Record):
    origin: LocationPayload()
    products: Array(OutboundProductPayload())

class CanceledOrderPayload(Record):
    order_id: String()
    products: Array(OutboundProductPayload())
    destination: LocationPayload()
    modification_date: Long()

class CreatedOutboundPayload(Record):
    order_id: String()
    warehouses: Array(WarehouseOrderPayload())
    destination: LocationPayload()
    created_date: Long()

class CanceledOutboundPayload(Record):
    order_id: String()
    warehouses: Array(WarehouseOrderPayload())
    destination: LocationPayload()
    modification_date: Long()

class CreatedOrderPayload(Record):
    products: Array(OutboundProductPayload())
    destiny: String()

class CreatedOrderEvent(IntegrationEvent()):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = CreatedOrderPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CanceledOrderEvent(IntegrationEvent):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = CanceledOrderPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class CreatedOutboundEvent(IntegrationEvent):
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

class CanceledOutboundEvent(IntegrationEvent):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = CanceledOutboundPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)