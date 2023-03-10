from __future__ import annotations
from dataclasses import dataclass, field
from order.dominio.entidades import Orden
from order.seedwork.dominio.eventos import (EventoDominio)
from datetime import datetime

class EventoOrden(EventoDominio):
    ...

@dataclass
class OrdenCreada(EventoOrden):
    ...

@dataclass
class OrdenListadoGenerado(EventoOrden):
    ordenes: list[Orden] = None
