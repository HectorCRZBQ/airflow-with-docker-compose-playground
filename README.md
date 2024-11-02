# Apache Airflow Playground

## Estructura de directorios

Ejecutamos el comando **ls** para revisar la estructura que debe coincidir con la siguiente

```
.
├── README.md
├── docker-compose.yaml
├── .env
├── dags/
│   └── population_pipeline.py
└── outputs/
    └── .gitignore
```

## Requisitos previos
- Docker
- Docker Compose
- Git

## Revisamos las versiones ejecutando los comandos

**Docker**
```
docker --version
```

![alt text](images/image1.png)

**Docker Compose**
```
docker compose --version
```

![alt text](images/image2.png)

**Git**
```
git --version
```

![alt text](images/image3.png)



## Puesta en marcha

1. Iniciar los servicios:
```bash
docker-compose up -d
```

![alt text](images/image4.png)

Revisamos que exista la imagen ejecutando el siguiente comando:
```bash
docker ps -a
```
![alt text](images/image5.png)

Revisamos que exista el contenedor ejecutando el siguiente comando:
```bash
docker images
```
![alt text](images/image6.png)


2. Ver los logs (incluye la contraseña de admin):
```bash
docker-compose logs airflow
```

![alt text](images/image7.png)

Se nos muestra que la contraseña para el usuario **admin** es **6mhF747TCazWph76**

*Si no se muestra la contraseña del usuario **admin** se ejecuta el siguiente comando para filtrar la busqueda:*
```bash
 docker-compose logs airflow | grep admin
```
![alt text](images/image8.png)


3. Acceder a la interfaz web:
- URL: http://localhost:8001

![alt text](images/image9.png)

- Usuario: admin
- Contraseña: buscar en los logs la línea que contiene "admin:password"

![alt text](images/image10.png)

## Verificar resultados

1. Ver el resultado en outputs:
```bash
cat outputs/report.txt
```

Al ejecutarlo me ha aparecido el siguiente error
![alt text](images/image11.png)

*Para corregirlo he ejecutado los siguientes comandos:*
```bash
chmod 775 outputs
ls -ld outputs
```
*Donde se dan permisos de lectura, escritura y ejeccución a outputs, y luego revisamos que los permisos se hayan actualizado.*

Lo volvemos a ejecutar para mostrar **report.txt**
```bash
cat outputs/report.txt
```
![alt text](images/image12.png)


2. O acceder directamente al contenedor:
```bash
docker-compose exec airflow bash
cat /tmp/report.txt
```
![alt text](images/image13.png)

## Detener los servicios

```bash
docker-compose down
```
![alt text](images/image14.png)

## Comandos útiles

- Ver logs en tiempo real:
```bash
docker-compose logs -f
```
![alt text](images/image15.png)

- Reiniciar servicios:
```bash
docker-compose restart
```
![alt text](images/image16.png)


- Limpiar todo (incluyendo volúmenes):
```bash
docker-compose down -v
```

# Nuevo DAG

Creamos un nuevo DAG que descarge datos de dos fuentes distintas, hace un merge de ambas y por ultimo genera un informe.

El nuevo dataset que hemos añadido es: https://github.com/datasets/world-cities/blob/main/data/world-cities.csv

En formato RAW: https://raw.githubusercontent.com/datasets/world-cities/refs/heads/main/data/world-cities.csv

Volvemos a iniciar los servicios:
```bash
docker-compose up -d
```
![alt text](images/image17.png)

Vemos los logs para conocer la contraseña del usuario **admin**
```bash
docker-compose logs airflow
```
![alt text](images/image18.png)

Se nos muestra que la contraseña para el usuario **admin** es **fkqYvKzbyvFCAcyx**

Accedemos a la interfaz web (http://localhost:8001) e iniciamos sesión con los credenciales obtenidos anteriormente

![alt text](images/image19.png)


Mostramos los outputs:
```bash
cat outputs/report.txt
```
![alt text](images/image20.png)

```bash
cat outputs/merged_report.txt
```
![alt text](images/image21.png)

Otra forma es acceder directamente al contenedor:
```bash
docker-compose exec airflow bash
cat /tmp/report.txt
```
![alt text](images/image22.png)


```bash
docker-compose exec airflow bash
cat /tmp/merged_report.txt
```

![alt text](images/image23.png)
