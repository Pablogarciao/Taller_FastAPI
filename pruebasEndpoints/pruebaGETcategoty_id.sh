#!/bin/bash

# URL base del endpoint
BASE_URL="http://localhost:8000/category/"

# Solicitar el ID de la categoría al usuario
read -p "Ingrese el ID de la categoría a buscar: " category_id

# Función para leer una categoría por ID
function read_category_by_id() {
  echo "Buscando la categoría con ID: $category_id"
  
  # Hacer la petición GET al endpoint
  response=$(curl -s -w "\n%{http_code}" -X GET "${BASE_URL}${category_id}")

  echo "Respuesta: $response"
}

# Ejecutar la prueba
read_category_by_id
