from pulsar.schema import *
from dataclasses import dataclass, field
from order.seedwork.infraestructura.schema.v1.comandos import (ComandoIntegracion)

class ComandoCrearOrdenPayload(ComandoIntegracion):
    id_usuario = String()
    # TODO Comandos de crearOrden y consultar ordenes

class ComandoCrearOrden(ComandoIntegracion):
    data = ComandoCrearOrdenPayload()