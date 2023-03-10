from ast import List
from pulsar.schema import *
from order.seedwork.infraestructura.schema.v1.eventos import EventoIntegracion
from order.seedwork.infraestructura.utils import time_millis
import uuid

class ProductoPayload(Record):
    productReference = String()
    amount = Integer()


class OrdenPayload(Record):
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
    data = OrdenPayload()

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
    data = Array(OrdenPayload())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)