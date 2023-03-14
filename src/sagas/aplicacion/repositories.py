from sagas.config.db import db
from sagas.aplicacion.dto import SagaLog

class RepositorioSagasSQLAlchemy():

    def agregar(self, record: SagaLog):
        db.session.add(record)
        db.session.commit()
