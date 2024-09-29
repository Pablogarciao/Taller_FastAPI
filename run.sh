#!/bin/bash

# Path Scripts
SCRIPT_PATH="./scripts" 

# Posibles Scripts
SETUP="setup"
DEV="dev"
START="start"

if [ "$1" == "$SETUP" ]; then
  echo "Ejecutando Script: $SCRIPT_PATH/$SETUP"
  bash "$SCRIPT_PATH/$SETUP.sh"
elif [ "$1" == "$DEV" ]; then
  echo "Ejecutando Script: $SCRIPT_PATH/$DEV"
  bash "$SCRIPT_PATH/$DEV.sh"
elif [ "$1" == "$START" ]; then
  echo "Ejecutando Script: $SCRIPT_PATH/$START"
  bash "$SCRIPT_PATH/$START.sh"
else
  echo "Parámetro inválido"
fi
