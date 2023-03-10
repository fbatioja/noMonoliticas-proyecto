from dataclasses import dataclass
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
class ObtenerReserva(Query):
    id: str

class ObtenerReservaHandler(OrdenQueryBaseHandler):
    def handle(self):
        repositorio = self.fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        ordenes = repositorio.obtener_todos()
        evento = OrdenListadoGenerado(ordenes=ordenes)
        despachador = Despachador()
        despachador.publicar_evento(evento, EventoListadoOrdenesGenerado, 'eventos-listado-orden-generado')
        return ordenes

@query.register(QueryGenerarListadoOrdenes)
def ejecutar_query_obtener_reserva(query: QueryGenerarListadoOrdenes):
    handler = ObtenerReservaHandler()
    return handler.handle()