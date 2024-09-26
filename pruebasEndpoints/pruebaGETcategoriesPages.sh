#!/bin/bash

# URL base del endpoint
BASE_URL="http://localhost:8000/categories/"

# Solicitar el número de página al usuario
read -p "Ingrese el número de página: " page

# Función para leer todas las categorías con paginación
function read_categories_by_page() {
  echo "Buscando categorías en la página: $page"
  
  # Hacer la petición GET al endpoint con el número de página
  response=$(curl -s -w "\n%{http_code}" -X GET "${BASE_URL}${page}")

  echo "Respuesta: $response"
}

# Ejecutar la prueba
read_categories_by_page
