import pulsar,_pulsar  
from pulsar.schema import *
import uuid
import time
import logging
import traceback
import datetime

from order.infraestructura.schema.v1.comandos import ComandoCrearOrden, QueryGenerarListadoOrdenes
from order.seedwork.aplicacion.comandos import ejecutar_commando
from order.seedwork.aplicacion.queries import ejecutar_query
from order.seedwork.infraestructura import utils

def suscribirse_a_comandos(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('crear-orden-comando', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='order-sub-comandos', schema=AvroSchema(ComandoCrearOrden))

        while True:
            mensaje = consumidor.receive()
            print(f'Comando recibido: {mensaje.value().data}')
            with app.app_context():
                ejecutar_commando(mensaje.value())
                consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de comandos!')
        traceback.print_exc()
        if cliente:
            cliente.close()

def suscribirse_a_queries(app=None):
    cliente = None
    try:
        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        consumidor = cliente.subscribe('listado-ordenes-generado-comando', consumer_type=_pulsar.ConsumerType.Shared, subscription_name='order-sub-queries', schema=AvroSchema(QueryGenerarListadoOrdenes))

        while True:
            mensaje = consumidor.receive()
            print(f'query recibido: {mensaje.value().data}')
            with app.app_context():
                ejecutar_query(mensaje.value())
                consumidor.acknowledge(mensaje)     

        cliente.close()
    except:
        logging.error('ERROR: Suscribiendose al tópico de queries!')
        traceback.print_exc()
        if cliente:
            cliente.close()
    
