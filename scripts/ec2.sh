#!/bin/bash

#? Levantar el proyecto en ec2

# Variables
VENV_DIR=$(realpath "$SCRIPT_DIR/../fastapi")

# Levantar
source $VENV_DIR/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
