#!/bin/bash

RUNNING=$(sudo systemctl status $SERVICE_NAME)

if [ "$EXIST" = "Unit $SERVICE_NAME could not be found." ]; then
  # Ejecutar el programa en modo desarrollo
  echo "Ejecutandose en modo dev: http://localhost:8000/docs"
  uvicorn main:app --reload
else
  sudo systemctl restart $SERVICE_NAME
  echo "Ejecutandose desde el $SERVICE_NAME: http://localhost:8000/docs"
fi