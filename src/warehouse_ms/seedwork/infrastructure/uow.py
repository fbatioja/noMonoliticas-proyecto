from abc import ABC, abstractmethod
from enum import Enum

from warehouse_ms.seedwork.domain.entities import RootAggregation
from pydispatch import dispatcher

import pickle
import logging
import traceback

class Lock(Enum):
    OPTIMIST = 1
    PESSIMISTIC = 2

class Batch:
    def __init__(self, operation, lock: Lock, *args, **kwargs):
        self.operation = operation
        self.args = args
        self.lock = lock
        self.kwargs = kwargs

class UnitOfWork(ABC):

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    def _get_rollback_events(self, batches=None):
        batches = self.batches if batches is None else batches
        events = list()
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, RootAggregation):
                    events += arg.compensation_events
                    break
        return events

    def _get_events(self, batches=None):
        batches = self.batches if batches is None else batches
        events = list()
        for batch in batches:
            for arg in batch.args:
                if isinstance(arg, RootAggregation):
                    events += arg.events
                    break
        return events

    @abstractmethod
    def _clean_batches(self):
        raise NotImplementedError

    @abstractmethod
    def batches(self) -> list[Batch]:
        raise NotImplementedError

    @abstractmethod
    def savepoints(self) -> list:
        raise NotImplementedError                    

    def commit(self):
        self._publish_post_commit_events()
        self._clean_batches()

    @abstractmethod
    def rollback(self, savepoint=None):
        self._clean_batches()
    
    @abstractmethod
    def savepoint(self):
        raise NotImplementedError

    def register_batch(self, operation, *args, lock=Lock.PESSIMISTIC, repository_events_func=None,**kwargs):
        batch = Batch(operation, lock, *args, **kwargs)
        self.batches.append(batch)
        self._publish_domain_events(batch, repository_events_func)

    def _publish_domain_events(self, batch, repository_events_func):
        for event in self._get_events(batches=[batch]):
            if repository_events_func:
                repository_events_func(event)
            dispatcher.send(signal=f'{type(event).__name__}Domain', event=event)

    def _publish_post_commit_events(self):
        try:
            for event in self._get_events():
                dispatcher.send(signal=f'{type(event).__name__}Integration', event=event)
        except:
            logging.error('ERROR: Subscribing to the topic of events!')
            traceback.print_exc()
            

def is_flask():
    try:
        from flask import session
        return True
    except Exception as e:
        return False

def register_unit_of_work(serialized_obj):
    from warehouse_ms.config.uow import UnitOfWorkSQLAlchemy
    from flask import session
    

    session['uow'] = serialized_obj

def flask_uow():
    from flask import session
    from warehouse_ms.config.uow import UnitOfWorkSQLAlchemy, UnitOfWorkPulsar
    if session.get('uow'):
        return session['uow']

    uow_serialized = pickle.dumps(UnitOfWorkSQLAlchemy())
    if session.get('uow_method') == 'pulsar':
        uow_serialized = pickle.dumps(UnitOfWorkPulsar())
    
    register_unit_of_work(uow_serialized)
    return uow_serialized

def unit_of_work() -> UnitOfWork:
    if is_flask():
        return pickle.loads(flask_uow())
    else:
        raise Exception('No unit of work found')

def save_unit_of_work(uow: UnitOfWork):
    if is_flask():
        register_unit_of_work(pickle.dumps(uow))
    else:
        raise Exception('No unit of work found')


class UnitOfWorkPort:

    @staticmethod
    def commit():
        uow = unit_of_work()
        uow.commit()
        save_unit_of_work(uow)

    @staticmethod
    def rollback(savepoint=None):
        uow = unit_of_work()
        uow.rollback(savepoint=savepoint)
        save_unit_of_work(uow)

    @staticmethod
    def savepoint():
        uow = unit_of_work()
        uow.savepoint()
        save_unit_of_work(uow)

    @staticmethod
    def get_savepoints():
        uow = unit_of_work()
        return uow.savepoints()

    @staticmethod
    def register_batch(operation, *args, lock=Lock.PESSIMISTIC, **kwargs):
        uow = unit_of_work()
        uow.register_batch(operation, *args, lock=lock, **kwargs)
        save_unit_of_work(uow)
