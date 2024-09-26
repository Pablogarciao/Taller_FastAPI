#!/bin/bash

# URL del endpoint
URL="http://localhost:8000/categories/"

# Datos válidos
VALID_DATA='{
  "category_name": "Aseo Personal",
  "description": "Jabon, Shampoo",
  "picture": ""
}'

# Datos inválidos (categoría existente)
INVALID_DATA='{
  "category_name": "Condiments",
  "description": "",
  "picture": ""
}'

# Función para probar creación de categoría con datos válidos
function test_valid() {
  echo "Probando con datos válidos..."
  response=$(curl -s -w "\n%{http_code}" -X POST $URL \
    -H "Content-Type: application/json" \
    -d "$VALID_DATA")

  echo "Respuesta: $response"
}

# Función para probar creación de categoría con datos inválidos
function test_invalid() {
  echo "Probando con datos inválidos (nombre de categoría existente)..."
  response=$(curl -s -w "\n%{http_code}" -X POST $URL \
    -H "Content-Type: application/json" \
    -d "$INVALID_DATA")

  echo "Respuesta: $response"
}

# Ejecutar las pruebas
test_valid
test_invalid
