
from __future__ import annotations
from dataclasses import dataclass, field
import datetime
import uuid

import order.dominio.objetos_valor as ov
from order.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class Producto(Entidad):
    referencia: uuid.UUID = field(hash=True, default=None)
    cantidad: int = field(default_factory=int)

@dataclass
class Orden(AgregacionRaiz):
    productos: list[Producto] = field(default_factory=list[Producto])
    destino: ov.Direccion = field(default_factory=ov.Direccion)
    estado: ov.EstadoOrden = field(default=ov.EstadoOrden.ENPROCESO)

    def crear_orden(self, orden: Orden):
        self.productos = orden.productos
        self.estado = orden.estado
        self.destino = orden.destino
        self.fecha_creacion = datetime.datetime.now()
