import datetime
import json
import os
import requests
from fastavro.schema import parse_schema
from pulsar.schema import *

def broker_host():
    return os.getenv('BROKER_HOST', default="localhost")

def millis_a_datetime(millis):
    return datetime.datetime.fromtimestamp(millis/1000.0)

def consultar_schema_registry(topico: str) -> dict:
    json_registry = requests.get(f'http://{broker_host()}:8080/admin/v2/schemas/{topico}/schema').json()
    print(json_registry)
    return json.loads(json_registry.get('data',{}))

from fastavro.schema import parse_schema
def obtener_schema_avro_de_diccionario(json_schema: dict) -> AvroSchema:
    definicion_schema = parse_schema(json_schema)
    return AvroSchema(None, schema_definition=definicion_schema)
