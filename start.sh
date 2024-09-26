#!/bin/bash

# Variables
SERVICE_PATH="/etc/systemd/system/$SERVICE_NAME"
PROJECT_PATH=$(pwd)

create_service() {
  # Paso 1: Crear archivo del servicio
  echo "Creando archivo de servicio en $SERVICE_PATH..."
  sudo bash -c "cat > $SERVICE_PATH" << EOL
[Unit]
Description=Taller_FastAPI service
After=network.target

[Service]
User=$USER
WorkingDirectory=$PROJECT_PATH
ExecStart=$PROJECT_PATH/fastapi/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOL

  echo "Archivo de servicio creado con éxito."

  # Paso 2: Recargar los servicios de systemd
  echo "Recargando los servicios de systemd..."
  sudo systemctl daemon-reload

  # Paso 3: Iniciar el servicio
  echo "Iniciando el servicio $SERVICE_NAME..."
  sudo systemctl start $SERVICE_NAME
  sudo systemctl enable $SERVICE_NAME

  # Paso 4: Habilitar el servicio para que se inicie al arrancar el sistema
  echo "Habilitando el servicio $SERVICE_NAME para que se inicie al arrancar..."

  # Paso 5: Verificar el estado del servicio
  echo "Verificando el estado del servicio..."
  sudo systemctl status $SERVICE_NAME
}

# Verificar si el service esta corriendo
EXIST=$(sudo systemctl status $SERVICE_NAME)

if [ "$EXIST" = "Unit $SERVICE_NAME could not be found." ]; then
  create_service
else
  sudo systemctl restart $SERVICE_NAME

  echo "Ejecutandose en: http://localhost:8000/docs"
fi
