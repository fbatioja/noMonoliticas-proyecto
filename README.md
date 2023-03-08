# Entrega proyecto

Este proyecto esta compuesto por 3 microservicios que se comunican usando eventos de dominio. Dentro de la carpeta src encontrara los tres microservicios: 

Orden
Bodega
Entrega 

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
flask --app src/warehouse/api run
```

5. Ejecutar microservicio de Bodega: Desde el directorio principal ejecute el siguiente comando.

```
flask --app src/warehouse/api run
```

6. Ejecutar microservicio de Entrega: Desde el directorio principal ejecute el siguiente comando.

```
flask --app src/warehouse/api run
```

# Como ejecutar la prueba

1. Use la colecciòn de postman AppsNoMonoliticas.json que se encuentra en la raiz y ejecute el metodo crear_orden_comando. Dado que para esta semana aun no tenemos el BFF ni la saga, esta funcion permite iniciar el proceso. El servicio de orden, recibe la peticiòn y en adelante la comunicaciòn si se da asincrona mediante eventos.