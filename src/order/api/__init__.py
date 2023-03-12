import os
import uuid
from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from order.dominio.entidades import Producto
from order.seedwork.dominio.excepciones import ExcepcionDominio
from flask import Response
import json
import pulsar
from pulsar.schema import *

basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import order.aplicacion

def comenzar_consumidor(app):
    import threading
    import order.infraestructura.consumidores as ordenes
    threading.Thread(target=ordenes.suscribirse_a_comandos, args=[app]).start()
    threading.Thread(target=ordenes.suscribirse_a_queries, args=[app]).start()


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
    from order.seedwork.aplicacion.queries import ejecutar_query
    from order.aplicacion.mapeadores import MapeadorOrdenDTOJson
    from order.infraestructura.schema.v1.comandos import QueryGenerarListadoOrdenes
    from order.aplicacion.queries.obtener_ordenes import ObtenerReserva
    from order.aplicacion.queries.obtener_ordenes_sincrona import ObtenerReservaSincrona

    @app.route('/orden-comando', methods=('POST',))
    def orden_asincrona():
        # Esta funcion se encuentra aca con propositos de pruebas.
        orden_dict = request.json
        map_orden = MapeadorOrdenDTOJson()
        orden_dto = map_orden.externo_a_dto(orden_dict)
        comando = CrearOrden(orden_dto.state, orden_dto.order_id, orden_dto.destiny, orden_dto.products)
        ejecutar_commando(comando) 
        return {"orden comando": "ok"}

    @app.route('/orden-query', methods=('GET',))
    def get_orden_sincrona():
        ordenes = ejecutar_query(ObtenerReservaSincrona(id=''))
        map = MapeadorOrdenDTOJson()
        return [map.dto_a_externo(orden) for orden in ordenes]

    return app