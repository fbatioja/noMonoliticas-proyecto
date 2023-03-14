from click import DateTime
from sagas.config.db import db
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Table

Base = db.declarative_base()

class SagaLog(db.Model):
    __tablename__ = 'saga_logs'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(36))
    message_id = db.Column(db.String(36))
    event = db.Column(db.String(50))
    started_at = db.Column(db.DateTime)
