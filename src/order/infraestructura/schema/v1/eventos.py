from ast import List
from pulsar.schema import *
from order.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from order.seedwork.infraestructura.utils import time_millis
import uuid

class ProductPayload(Record):
    productReference = String()
    amount = Integer()

class OrderPayload(Record):
    destiny = String()
    products =Array(ProductPayload())

class CreatedOrderEvent(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = OrderPayload()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class EventoListadoOrdenesGenerado(EventoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = Array(OrderPayload())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)