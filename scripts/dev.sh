#!/bin/bash

# Variables
SERVICE_NAME="taller_fastapi.service"
SCRIPT_DIR=$(dirname "$(realpath "$0")")
VENV_DIR=$(realpath "$SCRIPT_DIR/../fastapi")


SERVICE_STATUS=$(sudo systemctl is-active $SERVICE_NAME 2>&1)

if [ "$SERVICE_STATUS" = "active" ]; then
  sudo systemctl stop $SERVICE_NAME
fi


echo "Ejecutando en modo dev: http://localhost:8000/docs"
source $VENV_DIR/bin/activate
uvicorn main:app --reload
