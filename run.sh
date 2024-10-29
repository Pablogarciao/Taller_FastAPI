#!/bin/bash

# Path Scripts
SCRIPT_PATH="./scripts" 

# Posibles Scripts
SETUP="setup"
INSTALL="install"
DEV="dev"
START="start"
EC2="ec2"

if [ "$1" == "$SETUP" ]; then
  echo "Ejecutando Script: $SCRIPT_PATH/$SETUP"
  bash "$SCRIPT_PATH/$INSTALL.sh"
  bash "$SCRIPT_PATH/$SETUP.sh"

elif [ "$1" == "$DEV" ]; then
  echo "Ejecutando Script: $SCRIPT_PATH/$DEV"
  bash "$SCRIPT_PATH/$DEV.sh"

elif [ "$1" == "$START" ]; then
  echo "Ejecutando Script: $SCRIPT_PATH/$START"
  bash "$SCRIPT_PATH/$START.sh"

elif [ "$1" == "$EC2" ]; then
  echo "Ejecutando Script: $SCRIPT_PATH/$EC2"
  bash "$SCRIPT_PATH/$EC2.sh"
  
else
  echo "Parámetro inválido"
  echo -e "\nParámetros validos:"
  echo -e "\t$SETUP"
  echo -e "\t$DEV"
  echo -e "\t$START"
  echo -e "\t$EC2"
fi
