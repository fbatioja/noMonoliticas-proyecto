from dataclasses import dataclass, field
from .events import DomainEvent
from .mixins import ValidateRulesMixin
from .rules import IdEntityIsImmutable
from .exceptions import IdEntityIsImmutableException
from datetime import datetime
import uuid

@dataclass
class Entity:
    id: uuid.UUID = field(hash=True)
    _id: uuid.UUID = field(init=False, repr=False, hash=True)
    created_date: datetime =  field(default=datetime.now())
    modification_date: datetime = field(default=datetime.now())

    @classmethod
    def next_id(self) -> uuid.UUID:
        return uuid.uuid4()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: uuid.UUID) -> None:
        if not IdEntityIsImmutable(self).is_valid():
            raise IdEntityIsImmutableException()
        self._id = self.next_id()
        

@dataclass
class RootAggregation(Entity, ValidateRulesMixin):
    events: list[DomainEvent] = field(default_factory=list)
    compensation_events: list[DomainEvent] = field(default_factory=list)

    def add_event(self, event: DomainEvent, compensation_event: DomainEvent = None):
        self.events.append(event)

        if compensation_event:
            self.compensation_events.append(compensation_event)
    
    def clean_events(self):
        self.events = list()
        self.compensation_events = list()