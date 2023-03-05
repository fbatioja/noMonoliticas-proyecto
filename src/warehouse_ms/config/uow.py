from warehouse_ms.config.db import db
from warehouse_ms.seedwork.infrastructure.uow import UnitOfWork, Batch
from pydispatch import dispatcher

import logging
import traceback

class UoWException(Exception):
    ...

class UnitOfWorkSQLAlchemy(UnitOfWork):

    def __init__(self):
        self._batches: list[Batch] = list()

    def __enter__(self) -> UnitOfWork:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _clean_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        # TODO Lea savepoint
        return []

    @property
    def batches(self) -> list[Batch]:
        return self._batches             

    def commit(self):
        for batch in self.batches:
            lock = batch.lock
            batch.operacion(*batch.args, **batch.kwargs)
                
        db.session.commit() # Commits the transaction

        super().commit()

    def rollback(self, savepoint=None):
        if savepoint:
            savepoint.rollback()
        else:
            db.session.rollback()
        
        super().rollback()
    
    def savepoint(self):
        # TODO Con MySQL y Postgres se debe usar el with para tener la lógica del savepoint
        # Piense como podría lograr esto ¿tal vez teniendo una lista de savepoints y momentos en el tiempo?
        ...

class UnitOfWorkPulsar(UnitOfWork):

    def __init__(self):
        self._batches: list[Batch] = list()

    def __enter__(self) -> UnitOfWork:
        return super().__enter__()

    def __exit__(self, *args):
        self.rollback()

    def _clean_batches(self):
        self._batches = list()

    @property
    def savepoints(self) -> list:
        return []

    @property
    def batches(self) -> list[Batch]:
        return self._batches             

    def commit(self):
        index = 0
        try:
            for event in self._get_events():
                dispatcher.send(signal=f'{type(event).__name__}Integration', event=event)
                index += 1
        except:
            logging.error('ERROR: Subscribing to the topic of events!')
            traceback.print_exc()
            self.rollback(index=index)
        self._clean_batches()

    def rollback(self, index=None):
        # TODO Implemente la función de rollback
        # Vea los métodos agregar_evento de la clase AgregacionRaiz
        # A cada evento que se agrega, se le asigna un evento de compensación
        # Piense como podría hacer la implementación
        
        super().rollback()
    
    def savepoint(self):
        # NOTE No hay punto de implementar este método debido a la naturaleza de Event Sourcing
        ...