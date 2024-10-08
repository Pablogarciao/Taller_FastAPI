#!/bin/bash

# Salir en caso de error
set -e

# Variables locales
DB_NAME="Taller_FastAPI"
DB_CONTAINER_NAME="DB_Taller_FastAPI"
DB_USER="postgres"
DB_PASSWORD="password"
SCRIPT_DIR=$(dirname "$(realpath "$0")")
VENV_DIR=$(realpath "$SCRIPT_DIR/../fastapi")
SQL_FILE=$(realpath "$SCRIPT_DIR/../db/northwind.sql")

# Colores ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'


#? Creacion del Docker
echo -e "${BLUE}Creando contenedor de Docker...${NC}"
docker run --name $DB_CONTAINER_NAME -e POSTGRES_USER=$DB_USER -e POSTGRES_PASSWORD=$DB_PASSWORD -e POSTGRES_DB=$DB_NAME -p 5433:5432 --restart unless-stopped -d postgres

# Esperar a que el contenedor esté listo
echo -e "${BLUE}Esperando a que el contenedor esté listo...${NC}"
timeout=30  # Tiempo máximo en segundos
elapsed=0
while ! docker exec $DB_CONTAINER_NAME pg_isready -U $DB_USER; do
    sleep 1
    elapsed=$((elapsed + 1))
    if [ $elapsed -ge $timeout ]; then
        echo -e "Error: El contenedor no está listo después de $timeout segundos."
        exit 1
    fi
done


#? Copiar el archivo de la base de datos al contenedor
echo -e "\n${BLUE}Importando archivo SQL en Docker...${NC}"
docker cp $SQL_FILE $DB_CONTAINER_NAME:/northwind.sql

# Importar archivo northwind.sql en PostgreSQL
echo -e "${BLUE}Importando la base de datos...${NC}"
docker exec -i $DB_CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -f /northwind.sql


#? Crear entorno virtual
echo -e "\n${BLUE}Creando entorno virtual...${NC}"
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Instalar librerías
echo -e "${BLUE}Instalando librerías...${NC}"
pip install -r requirements.txt


#? Ejecucion del programa
echo -e "\n\n${GREEN}Todo está configurado para correr la aplicación.${NC}"

echo -e "\nPara ejecutar en modo dev:"
echo -e "\t${GREEN}bash run.sh dev${NC}"

echo -e "\nPara levantar en modo produccion"
echo -e "\t${GREEN}bash run.sh start${NC}"
