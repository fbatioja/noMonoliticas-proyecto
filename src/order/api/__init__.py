import os
import uuid

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from order.dominio.entidades import Producto

#TODO: remover cuando se implemento completo y orden este escuchando el evento
from order.seedwork.dominio.excepciones import ExcepcionDominio
from flask import Response
import json
import pulsar
from pulsar.schema import *
#end TODO

basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import order.aplicacion

def comenzar_consumidor(app):
    import threading
    import order.infraestructura.consumidores as vuelos
    threading.Thread(target=vuelos.suscribirse_a_comandos, args=[app]).start()


def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from order.config.db import init_db, database_connection
    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection(configuracion, basedir=basedir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from order.config.db import db
    import order.infraestructura.dto
    import order.aplicacion

    registrar_handlers()
    
    with app.app_context():
        db.create_all()       

        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

    @app.route("/health")
    def health():
        return {"status": "up"}


    from order.aplicacion.comandos.crear_orden import CrearOrden
    from order.seedwork.aplicacion.comandos import ejecutar_commando
    from order.aplicacion.mapeadores import MapeadorOrdenDTOJson
    @app.route('/orden-comando', methods=('POST',))
    def orden_asincrona():       
        print('Entro aca')
        #orden_dict = request.json
#        map_orden = MapeadorOrdenDTOJson()
#        orden_dto = map_orden.externo_a_dto(orden_dict)
        #comando = CrearOrden(orden_dto.state, orden_dto.order_id, orden_dto.destiny, orden_dto.products)


        import pulsar
        from order.infraestructura.schema.v1.comandos import ComandoCrearOrden, ComandoCrearOrdenPayload, ComandoProductoPayload
        from order.seedwork.infraestructura import utils
        from order.seedwork.infraestructura.utils import unix_time_millis


        productsPayload = []
        productoPayload = ComandoProductoPayload(
                amount=10,
                productReference='5bfb499c-bd2a-11ed-afa1-0242ac120002'
            )
        productsPayload.append(productoPayload)    
        payload = ComandoCrearOrdenPayload( 
            destiny='Calle 3 # 9-92', 
            products=productsPayload, 
        )
        comando = ComandoCrearOrden()

        comando.data = payload

        cliente = pulsar.Client(f'pulsar://{utils.broker_host()}:6650')
        publicador = cliente.create_producer('comandos-orden', schema=AvroSchema(ComandoCrearOrden))
        publicador.send(comando)


        #ejecutar_commando(comando)
        return {"orden comando": "ok"}
        

    return app