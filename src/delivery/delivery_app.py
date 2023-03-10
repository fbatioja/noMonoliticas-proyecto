from schemas import CreatedOutboundEvent
from delivery_controller import processCreateDelivery
import psycopg2
from psycopg2 import Error
import pulsar,_pulsar  
from pulsar.schema import *
import json
import os

db_user = os.environ.get('DB_USER', 'delivery_user')
db_password = os.environ.get('DB_PASSWORD', '987654321')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', '5432')
db_name = os.environ.get('DB_NAME', 'delivery_db')

pulsar_host = os.environ.get('PULSAR_HOST', 'pulsar://localhost:6650')
pulsar_subs_topic = os.environ.get('PULSAR_SUBS_TOPIC', 'outbound-created')
pulse_subs_name = os.environ.get('PULSAR_SUBS_NAME', 'delivery-sub')

try:
    # Connect to an existing database
    connection = psycopg2.connect(user=db_user,
                                  password=db_password,
                                  host=db_host,
                                  port=db_port,
                                  database=db_name)

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    create_table_query = '''CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
          CREATE TABLE IF NOT EXISTS road_map
          (
          id UUID DEFAULT uuid_generate_v4 (),
          order_id UUID NOT NULL,
          PRIMARY KEY ( id )); 

          DO $$ BEGIN
            CREATE TYPE delivery_status AS ENUM('CREATED','IN_PROGRES','CANCELED','DECLINED');
        EXCEPTION
            WHEN duplicate_object THEN null;
        END $$;

          
          
          CREATE TABLE IF NOT EXISTS delivery
          (
          id UUID DEFAULT uuid_generate_v4 (),
          road_map_id UUID NOT NULL,
          origin VARCHAR(255) NOT NULL,
          destination VARCHAR(255) NOT NULL,
          status delivery_status NOT NULL,
          PRIMARY KEY ( id ),
          FOREIGN KEY (road_map_id) REFERENCES road_map (id)
          );

          CREATE TABLE IF NOT EXISTS product
          (
          product_reference UUID DEFAULT uuid_generate_v4 (),
          delivery_id UUID NOT NULL,
          amount INT NOT NULL,
          PRIMARY KEY ( product_reference, delivery_id ),
            FOREIGN KEY (delivery_id) REFERENCES DELIVERY (id)
          );
          '''
    # Execute a command: this creates a new table
    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL ")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

client = pulsar.Client(pulsar_host)
consumer = client.subscribe(pulsar_subs_topic, consumer_type=_pulsar.ConsumerType.Shared, subscription_name=pulse_subs_name, schema=AvroSchema(CreatedOutboundEvent))

while True:
    msg = consumer.receive()    
    data = msg.value().data
    print(f'Received event: {data}')
    processCreateDelivery(cursor, connection, data)
    print("Order processed...")
    consumer.acknowledge(msg)

client.close()
 