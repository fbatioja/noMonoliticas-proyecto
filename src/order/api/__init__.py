import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, session

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    
    # TODO: Remover o saber que hace esto
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

    with app.app_context():
        print(db)
        db.create_all()
        from order.dominio.entidades import Orden
        from order.dominio.objetos_valor import Direccion
        from order.dominio.objetos_valor import EstadoOrden
        from order.dominio.repositorios import RepositorioOrdenes
        from order.infraestructura.fabricas import FabricaRepositorio
        orden = Orden(destino=Direccion("direccion string"), estado=EstadoOrden.ENPROCESO)
        orden.estado = EstadoOrden.ENPROCESO
        orden.productos = []
        fabrica_repositorio: FabricaRepositorio = FabricaRepositorio()

        repositorio = fabrica_repositorio.crear_objeto(RepositorioOrdenes)
        repositorio.agregar(orden)


        if not app.config.get('TESTING'):
            #comenzar_consumidor(app)
            pass

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app