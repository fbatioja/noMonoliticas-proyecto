import pulsar,_pulsar  
from pulsar.schema import *
import logging
import traceback
from bff_web import utils
from sagas.aplicacion.coordinadores.saga_reservas import CoordinadorReservas
from sagas.util import consultar_schema_registry, obtener_schema_avro_de_diccionario


def suscribirse_a_ordenes(app=None):
    suscribirse_a_topico('order-created','sagas','public/default/order-created', app)

def suscribirse_a_bodega(app=None):
    suscribirse_a_topico('outbound-created','sagas','public/default/outbound-created', app)

def suscribirse_a_entrega(app=None):
    suscribirse_a_topico('roadmap-created','sagas','public/default/roadmap-created', app)

def suscribirse_a_entrega_fallos(app=None):
    suscribirse_a_topico('order-canceled','sagas','public/default/order-canceled', app)


def suscribirse_a_topico(topico, suscriptionName, schema, app=None):
    cliente = None
    try:
        if schema is not None:
            json_schema = consultar_schema_registry(schema)  
            avro_schema = obtener_schema_avro_de_diccionario(json_schema)
            cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
            consumidor = cliente.subscribe(topico, consumer_type=_pulsar.ConsumerType.Shared, subscription_name=suscriptionName, schema=avro_schema)
        else:
            cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
            consumidor = cliente.subscribe(topico, consumer_type=_pulsar.ConsumerType.Shared, subscription_name=suscriptionName)

        while True:
            mensaje = consumidor.receive()
            with app.app_context():
                coordinador = CoordinadorReservas()
                coordinador.persistir_en_saga_log(mensaje.value())
                consumidor.acknowledge(mensaje)     
        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de {}!'.format(topico))
        traceback.print_exc()
        if cliente:
            cliente.close()
