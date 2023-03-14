import os
from flask import Flask
from flask import Response
from pulsar.schema import *

basedir = os.path.abspath(os.path.dirname(__file__))

def comenzar_consumidor(app):
    import sagas.consumidores as ordenes
    import threading

    threading.Thread(target=ordenes.suscribirse_a_ordenes, args=[app]).start()
    #threading.Thread(target=ordenes.suscribirse_a_bodega, args=[app]).start()
    #threading.Thread(target=suscribirse_a_entrega, args=[app]).start()
    #threading.Thread(target=suscribirse_a_entrega_fallos, args=[app]).start()

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from sagas.config.db import init_db, database_connection
    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection(configuracion, basedir=basedir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from sagas.config.db import db
    import sagas.aplicacion.dto
    
    with app.app_context():
        db.create_all()       

        if not app.config.get('TESTING'):
            comenzar_consumidor(app)

    return app
