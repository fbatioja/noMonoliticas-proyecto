import psycopg2
from psycopg2 import Error
import pulsar
from pulsar.schema import *
import json
import os
from schemas import CanceledOrderEvent,OrdenCanceladaPayload,ProductoPayload, CreatedDeliveryEvent, DeliveryPayload, RoadmapPayload
import time
import os
import datetime
import uuid

epoch = datetime.datetime.utcfromtimestamp(0)

pulsar_host = os.environ.get('PULSAR_HOST', 'pulsar://localhost:6650')
pulsar_pub_topic = os.environ.get('PULSAR_SUBS_TOPIC', 'roadmap-created')

def unix_time_millis(dt):
    return (dt - epoch).total_seconds() * 1000.0

def sendRoadMapCreatedEvent(data):
    client = pulsar.Client(pulsar_host)
    producer = client.create_producer('roadmap-created', schema=AvroSchema(CreatedDeliveryEvent))

    deliveries = []
    for delivery in data['deliveries']:
        deliveries.append(DeliveryPayload(delivery_id=delivery['id'], status=delivery['status']))

    sendedData = RoadmapPayload(order_id=data['order_id'], roadmap_id=data['roadMapId'], deliveries=deliveries)

    integration_event = CreatedDeliveryEvent(id=str(uuid.uuid4()))
    integration_event.time = int(unix_time_millis(datetime.datetime.now()))
    integration_event.specversion = str('v1')
    integration_event.type = 'CreatedDelivery'
    integration_event.datacontenttype = 'AVRO'
    integration_event.service_name = 'eds'
    integration_event.data = sendedData

    producer.send(integration_event)
    client.close()


def createRoadMapDB(cursor, connection, orderId):
    cursor.execute("INSERT INTO ROAD_MAP (order_id ) VALUES (%s) RETURNING id", (orderId,))
    connection.commit()
    lastid = cursor.fetchone()[0]
    return lastid

def processCreateDelivery(cursor, connection, data):
    roadMapId = createRoadMapDB(cursor, connection, data.order_id)
    roadmapData = {"roadMapId": roadMapId, "deliveries": [], "order_id": data.order_id}
    for warehouse in data.warehouses:
        cursor.execute("INSERT INTO DELIVERY (road_map_id, origin, destination, status) VALUES (%s, %s, %s, %s) RETURNING id", (roadMapId, warehouse.origin, data.destination, 'CREATED'))
        connection.commit()
        deliveryId = cursor.fetchone()[0]
        roadmapData['deliveries'].append({"id": deliveryId, "status": 'CREATED'})
        for product in warehouse.products:
            cursor.execute("INSERT INTO PRODUCT (product_reference,delivery_id, amount) VALUES (%s,%s, %s)", (product.productReference, deliveryId, product.amount))
            connection.commit()

    sendRoadMapCreatedEvent(roadmapData)
    print(roadmapData)
    print("Delivery created successfully in PostgreSQL, road map id: ", roadMapId)

def sendCanceledOutboundEvent(data):
    products = []
    for warehouse in data.warehouses:
        for product in warehouse.products:
            product_payload = ProductoPayload(
                productReference = product.productReference,
                amount = product.amount
            )
            products.append(product_payload)

    payload = OrdenCanceladaPayload(order_id=data.order_id , destiny=data.destination, products=products)

    integration_event = CanceledOrderEvent(id=str(uuid.uuid4()))
    integration_event.time = int(unix_time_millis(datetime.datetime.now()))
    integration_event.specversion = str('v1')
    integration_event.type = 'CanceledOrder'
    integration_event.datacontenttype = 'AVRO'
    integration_event.service_name = 'eds'
    integration_event.data = payload    

    client = pulsar.Client(pulsar_host)
    producer = client.create_producer('order-canceled', schema=AvroSchema(CanceledOrderEvent))
    producer.send(integration_event)
    client.close()