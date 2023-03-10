from order.infraestructura.schema.v1.eventos import EventoOrdenCreada
from order.seedwork.aplicacion.handlers import Handler
from order.infraestructura.despachadores import Despachador

class HandlerOrdenIntegracion(Handler):

    @staticmethod
    def handle_orden_creada(evento):
        despachador = Despachador()
        despachador.publicar_evento(evento, EventoOrdenCreada, 'eventos-orden')
