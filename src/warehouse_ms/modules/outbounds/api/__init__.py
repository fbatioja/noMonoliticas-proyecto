import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger


# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def register_handlers():
    import warehouse_ms.modules.outbounds.application

def import_alchemy_models():
    import warehouse_ms.modules.outbounds.infrastructure.dto

def start_consumers(app):
    import threading
    import warehouse_ms.modules.outbounds.infrastructure.consumers as outbounds

    # Events subscriptions
    threading.Thread(target=outbounds.subscribe_to_created_order_event, args=[app]).start()

    # Commands subscriptions

def create_app(configuracion={}):
    # Init Flask application
    app = Flask(__name__, instance_relative_config=True)
    
    app.secret_key = '9d58f98f-3ae8-4149-a09f-3a8c2012e32c'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['TESTING'] = configuracion.get('TESTING')

     # Inicializa la DB
    from warehouse_ms.config.db import init_db, database_connection

    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection(configuracion, basedir=basedir)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    init_db(app)

    from warehouse_ms.config.db import db

    import_alchemy_models()
    register_handlers()

    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING'):
            start_consumers(app)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "My API"
        return jsonify(swag)

    @app.route("/health")
    def health():
        return {"status": "up"}

    return app
