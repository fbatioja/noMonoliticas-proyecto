# Entrega proyecto

Este proyecto esta compuesto por 3 microservicios que se comunican usando eventos de dominio. Dentro de la carpeta src encontrara los tres microservicios: 

Order
Warehouse
Delivery 

# Pasos para ejecutar aplicaciòn
1. Ejecutar apache Pulsar
```
docker-compose --profile pulsar up
```
2. Crear base de datos MySQL
```
docker-compose --profile db up
```
3. Ejecutar microservicio de ordenes: Desde el directorio principal ejecute el siguiente comando.

```
flask --app src/order/api run
```
4. Ejecutar microservicio de Bodega: Desde el directorio principal ejecute el siguiente comando.

```
flask --app ./src/warehouse_ms/modules/outbounds/api run --host=0.0.0.0 (editado) 
```

5. Ejecutar microservicio de Delivery: Desde el directorio principal ejecute el siguiente comando.

## Microservicio de Delivery 
Definición de variables de entornos: Defina las varibles de entorno ejecutando los siguientes comandos en la terminal o dejando por default los valores para la conección

```
export DB_USER=delivery_user
export DB_PASSWORD=987654321
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=delivery_db
export PULSAR_HOST=pulsar://localhost:6650
export PULSAR_SUBS_TOPIC=outbound-created
export DB_PASSWORD=delivery-sub
export PULSAR_SUBS_TOPIC=roadmap-created
```
Ejecutar microservicio:
```
python src/delivery/delivery_app.py
```

6. Ejecutar BFF: Desde `src/` ejecute el siguiente comando.
```
uvicorn bff_web.main:app --host localhost --port 8003 --reload
```
# Como ejecutar la prueba

1. Use la colecciòn de postman AppsNoMonoliticas.json que se encuentra en la raiz y ejecute el metodo crear_orden_comando. Dado que para esta semana aun no tenemos el BFF ni la saga, esta funcion permite iniciar el proceso. El servicio de orden, recibe la peticiòn y en adelante la comunicaciòn si se da asincrona mediante eventos.