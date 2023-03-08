import uuid

from pulsar.schema import *
from warehouse_ms.seedwork.infrastructure.utils import time_millis

class Message(Record):
    id = String(default=str(uuid.uuid4()))
    time = Long()
    ingestion = Long(default=time_millis())
    specversion = String()
    type = String()
    datacontenttype = String()
    service_name = String()

    def __init__(self, *args, id=None, **kwargs):
        super().__init__(*args, id=id, **kwargs)