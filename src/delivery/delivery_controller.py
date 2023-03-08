import psycopg2
from psycopg2 import Error
import pulsar
import json
import os

pulsar_host = os.environ.get('PULSAR_HOST', 'pulsar://localhost:6650')
pulsar_pub_topic = os.environ.get('PULSAR_SUBS_TOPIC', 'roadmap-created')

def sendRoadMapCreatedEvent(data):
    client = pulsar.Client(pulsar_host)
    producer = client.create_producer(pulsar_pub_topic)
    sendedData = {
        "roadmap_id": data['roadMapId'],
        "deliveries": [],
    }
    for delivery in data['deliveries']:
        sendedData['deliveries'].append({
            "delivery_id": delivery['id'],
            "status": delivery['status'],
        })
    print(sendedData)
    producer.send(json.dumps(sendedData).encode('utf-8'))
    client.close()


def createRoadMapDB(cursor, connection, orderId):
    cursor.execute("INSERT INTO ROAD_MAP (order_id ) VALUES (%s) RETURNING id", (orderId,))
    connection.commit()
    lastid = cursor.fetchone()[0]
    return lastid

def processCreateDelivery(cursor, connection, data):

    roadMapId = createRoadMapDB(cursor, connection, data['orderId'])
    roadmapData = {"roadMapId": roadMapId, "deliveries": []}
    for warehouse in data['warehouses']:
        cursor.execute("INSERT INTO DELIVERY (road_map_id, origin, destination, status) VALUES (%s, %s, %s, %s) RETURNING id", (roadMapId, warehouse['origin'], data['destiny'], 'CREATED'))
        connection.commit()
        deliveryId = cursor.fetchone()[0]
        roadmapData['deliveries'].append({"id": deliveryId, "status": 'CREATED'})
        for product in warehouse['products']:
            cursor.execute("INSERT INTO PRODUCT (product_reference,delivery_id, amount) VALUES (%s,%s, %s)", (product['productReference'], deliveryId, product['amount']))
            connection.commit()

    sendRoadMapCreatedEvent(roadmapData)
    print(roadmapData)
    print("Delivery created successfully in PostgreSQL, road map id: ", roadMapId)
