import requests

# URL base del endpoint
BASE_URL = "http://localhost:8000/categories/"

def delete_category(category_id):
    print(f"Eliminando la categoría con ID: {category_id}...")
    
    # Hacer la solicitud DELETE
    response = requests.delete(f"{BASE_URL}{category_id}")
    
    # Verificar el código de estado de la respuesta
    print(f"Response status code: {response.status_code}")
    
    # Imprimir la respuesta completa para inspección
    print(f"Respuesta completa: {response.json()}")
    
    # Comprobar el estado de la respuesta
    if response.status_code == 200:
        response_json = response.json()
        print(f"Test passed: {response_json['message']}")
        print(f"Categoría eliminada: {response_json['data']}")
    elif response.status_code == 404:
        print(f"Test failed: {response.json()['detail']}")
    else:
        print(f"Error: {response.status_code}")

# Prueba de eliminación
delete_category(9)  # Cambia el ID según la categoría que quieras eliminar