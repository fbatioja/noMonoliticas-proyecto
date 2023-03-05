from __future__ import annotations

from dataclasses import dataclass, field
from order.seedwork.dominio.objetos_valor import ObjetoValor
from datetime import datetime
from enum import Enum

@dataclass(frozen=True)
class Direccion(ObjetoValor):
    direccion: str

class EstadoOrden(Enum):
    ENPROCESO = "En proceso"
    COMPLETADO = "Completado"
    FALLIDO = "Fallido"
