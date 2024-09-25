#!/bin/bash

# Salir en caso de error
set -e

# Variables
DB_NAME="Taller_FastAPI"
DB_CONTAINER_NAME="DB_Taller_FastAPI"
DB_USER="postgres"
DB_PASSWORD="password"
SQL_FILE="./northwind.sql"
VENV_DIR="fastapi"


#? Creacion del Docker
echo "Creando contenedor de Docker..."
docker run --name $DB_CONTAINER_NAME -e POSTGRES_USER=$DB_USER -e POSTGRES_PASSWORD=$DB_PASSWORD -e POSTGRES_DB=$DB_NAME -p 5433:5432 -d postgres

# Esperar a que el contenedor esté listo
echo "Esperando a que el contenedor esté listo..."
timeout=30  # Tiempo máximo en segundos
elapsed=0
while ! docker exec $DB_CONTAINER_NAME pg_isready -U $DB_USER; do
    sleep 1
    elapsed=$((elapsed + 1))
    if [ $elapsed -ge $timeout ]; then
        echo "Error: El contenedor no está listo después de $timeout segundos."
        exit 1
    fi
done


#? Copiar el archivo de la base de datos al contenedor
echo "Importando archivo SQL en Docker..."
docker cp $SQL_FILE $DB_CONTAINER_NAME:/northwind.sql

# Importar archivo northwind.sql en PostgreSQL
echo "Importando la base de datos..."
docker exec -i $DB_CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -f /northwind.sql


#? Crear entorno virtual
echo "Creando entorno virtual..."
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Instalar librerías
echo "Instalando librerías..."
pip install pandas fastapi uvicorn sqlalchemy psycopg2-binary asyncpg


#? Mensaje final
echo "Todo está configurado. Para correr la aplicación, ejecuta:"
echo "uvicorn main:app --reload"
