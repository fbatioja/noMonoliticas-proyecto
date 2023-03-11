import pulsar
import json

client = pulsar.Client('pulsar://localhost:6650')
producer = client.create_producer('outbound-created')
data = {
    "orderId": 'e14c15a0-a98a-4d26-8b42-8443851ad1c6',
    "warehouses": [{
        "origin": 'Warehouse 1',
        "products": [
            {"productReference": 'e14c15a0-a98a-4d26-8b42-8443851ad1c6',
             "amount": 10},
             {"productReference": '73921880-353d-4877-b4ea-fe4c6b03bc21',
             "amount": 10}
        ],
    },
        {
        "origin": 'Warehouse 2',
        "products": [
            {"productReference": 'e14c15a0-a98a-4d26-8b42-8443851ad1c6',
             "amount": 10},
             {"productReference": '73921880-353d-4877-b4ea-fe4c6b03bc21',
             "amount": 10}
        ],
    }],
    "destiny": 'Destino final'
}

producer.send(json.dumps(data, separators=(',', ':')).encode('utf-8'))

client.close()
