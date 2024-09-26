#!/bin/bash

# URL base del endpoint
BASE_URL="http://localhost:8000/categories/"

#ID categoria a eliminar
category_id=9  

# Función para eliminar una categoría por ID
function delete_category_by_id() {
  echo "Eliminando la categoría con ID: $category_id"
  
  # Hacer la petición DELETE al endpoint
  response=$(curl -s -w "\n%{http_code}" -X DELETE "${BASE_URL}${category_id}")

  echo "Respuesta: $response"
}

# Ejecutar la prueba
delete_category_by_id
