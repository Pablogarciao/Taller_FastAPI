#!/bin/bash

# Variables
SCRIPT_DIR=$(dirname "$(realpath "$0")")
VENV_DIR=$(realpath "$SCRIPT_DIR/../fastapi")
PROJECT_PATH=$(realpath "$SCRIPT_DIR/../")

SERVICE_NAME="taller_fastapi.service"
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"

# Colores ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

create_service() {
  # Paso 1: Crear archivo del servicio
  echo -e "${BLUE}\nCreando archivo de servicio en $SERVICE_PATH...${NC}"
  sudo bash -c "cat > $SERVICE_PATH" << EOL
[Unit]
Description=Taller_FastAPI service
After=network.target

[Service]
User=$USER
WorkingDirectory=$PROJECT_PATH
ExecStart=$VENV_DIR/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOL

  # Paso 2: Recargar los servicios de systemd
  echo -e "${BLUE}\nRecargando los servicios de systemd...${NC}"
  sudo systemctl daemon-reload

  # Paso 3: Iniciar el servicio
  echo -e "${BLUE}\nIniciando el servicio $SERVICE_NAME...${NC}"
  sudo systemctl start $SERVICE_NAME
  sudo systemctl enable $SERVICE_NAME

  # Paso 4: Habilitar el servicio para que se inicie al arrancar el sistema
  echo -e "${BLUE}\nHabilitando el servicio $SERVICE_NAME para que se inicie al arrancar...${NC}"
  sudo systemctl enable $SERVICE_NAME

  # Paso 5: Verificar el estado del servicio
  echo -e "${BLUE}\nVerificando el estado del servicio...${NC}"
  sudo systemctl status $SERVICE_NAME
}

# Verificar si el service esta corriendo
SERVICE_STATUS=$(sudo systemctl is-active $SERVICE_NAME 2>&1)

if [ "$SERVICE_STATUS" = "active" ]; then
  sudo systemctl restart $SERVICE_NAME
else
  create_service
fi

echo -e "${GREEN}\nEjecutandose desde el servicio en: http://localhost:8000/docs${NC}"

read -p "Le gustaria levantar el servicio con NGROK? [y/n] " NGROK

if [[ "$NGROK" == "y" || "$NGROK" == "Y" || -z "$NGROK" ]]; then
  echo -e "${GREEN}Levantando el servicio con NGROK...${NC}"
  ngrok http http://localhost:8000
else
  echo -e "${RED}No se levantará el servicio con NGROK.${NC}"
fi
