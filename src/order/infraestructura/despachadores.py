import pulsar
from pulsar.schema import *

from order.infraestructura.schema.v1.eventos import EventoOrdenCreada
from order.seedwork.infraestructura import utils

from order.infraestructura.mapeadores import MapadeadorEventosOrden

class Despachador:
    def __init__(self):
        self.mapper = MapadeadorEventosOrden()

    def _publicar_mensaje(self, mensaje, topico, schema):
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer(topico, schema=schema)
        publicador.send(mensaje)
        cliente.close()


    def publicar_evento(self, evento, tipo, topico):
        evento = self.mapper.entidad_a_dto(evento)
        self._publicar_mensaje(evento, topico, AvroSchema(tipo))
