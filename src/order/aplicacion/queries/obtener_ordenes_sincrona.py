from dataclasses import dataclass
from order.aplicacion.mapeadores import MapeadorOrden
from order.aplicacion.queries.base import OrdenQueryBaseHandler
from order.dominio.eventos import OrdenListadoGenerado
from order.infraestructura.despachadores import Despachador
from order.infraestructura.schema.v1.comandos import QueryGenerarListadoOrdenes
from order.infraestructura.schema.v1.eventos import EventoListadoOrdenesGenerado
from order.seedwork.aplicacion.queries import Query, QueryHandler
from order.seedwork.aplicacion.queries import ejecutar_query as query
from order.dominio.repositorios import RepositorioOrdenes
from pydispatch import dispatcher
import uuid

@dataclass
class ObtenerReservaSincrona(Query):
    id: str

class ObtenerReservaHandler(OrdenQueryBaseHandler):
    def handle(self):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        ordenes = repositorio.obtener_todos()
        map = MapeadorOrden()
        return  [map.entidad_a_dto(orden) for orden in ordenes]

@query.register(ObtenerReservaSincrona)
def ejecutar_query_obtener_reserva(query: ObtenerReservaSincrona):
    handler = ObtenerReservaHandler()
    return handler.handle()