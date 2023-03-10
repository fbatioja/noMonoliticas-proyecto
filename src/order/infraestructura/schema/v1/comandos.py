import uuid
from pulsar.schema import *
from dataclasses import dataclass, field
from order.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)
from order.seedwork.infraestructura.utils import time_millis

class ComandoProductoPayload(Record):
    productReference = String()
    amount = Integer()

class ComandoCrearOrdenPayload(Record):
    destiny = String()
    products =Array(ComandoProductoPayload())

class ComandoCrearOrden(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = ComandoCrearOrdenPayload()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    data = ComandoCrearOrdenPayload()

class QueryGenerarListadoOrdenes(ComandoIntegracion):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()
    data = String()
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)