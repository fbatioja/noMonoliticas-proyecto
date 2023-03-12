from bff_web.utils import millis_a_datetime
from sagas.aplicacion.dto import SagaLog
from sagas.aplicacion.repositories import RepositorioSagasSQLAlchemy


class CoordinadorReservas():

    def persistir_en_saga_log(self, mensaje: dict):
        print(mensaje)
        repositorio = RepositorioSagasSQLAlchemy()
        record = SagaLog()
        record.transaction_id = mensaje.get('data', {}).get('order_id') 
        record.message_id = mensaje.get('id')
        record.event = mensaje.get('type')
        record.started_at = millis_a_datetime(mensaje.get('ingestion'))
        repositorio.agregar(record)

