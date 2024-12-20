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

# Asegúrate de que Docker esté en funcionamiento
echo -e "${BLUE}Iniciando Docker...${NC}"
sudo systemctl start docker

#? Creación del contenedor de Docker
echo -e "${BLUE}Creando contenedor de Docker...${NC}"
sudo docker run --name $DB_CONTAINER_NAME \
    -e POSTGRES_USER=$DB_USER \
    -e POSTGRES_PASSWORD=$DB_PASSWORD \
    -e POSTGRES_DB=$DB_NAME \
    -p 5433:5432 --restart unless-stopped -d postgres

# Esperar a que el contenedor esté listo
echo -e "${BLUE}Esperando a que el contenedor esté listo...${NC}"
timeout=30  # Tiempo máximo en segundos
elapsed=0
while ! sudo docker exec $DB_CONTAINER_NAME pg_isready -U $DB_USER; do
    sleep 1
    elapsed=$((elapsed + 1))
    if [ $elapsed -ge $timeout ]; then
        echo -e "${RED}Error: El contenedor no está listo después de $timeout segundos.${NC}"
        exit 1
    fi
done

#? Copiar el archivo SQL al contenedor
echo -e "\n${BLUE}Importando archivo SQL en Docker...${NC}"
sudo docker cp $SQL_FILE $DB_CONTAINER_NAME:/northwind.sql

# Importar archivo SQL en la base de datos PostgreSQL
echo -e "${BLUE}Importando la base de datos...${NC}"
sudo docker exec -i $DB_CONTAINER_NAME psql -U $DB_USER -d $DB_NAME -f /northwind.sql

#? Crear entorno virtual
echo -e "\n${BLUE}Creando entorno virtual...${NC}"
sudo python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate

# Instalar librerías
echo -e "${BLUE}Instalando librerías...${NC}"
pip install --upgrade pip  # Asegúrate de que pip esté actualizado
pip install -r $SCRIPT_DIR/../requirements.txt

#? Ejecución final
echo -e "\n\n${GREEN}Todo está configurado para correr la aplicación.${NC}"
echo -e "\nPara ejecutar en modo dev:"
echo -e "\t${GREEN}bash run.sh dev${NC}"

echo -e "\nPara levantar en modo producción:"
echo -e "\t${GREEN}bash run.sh start${NC}"
