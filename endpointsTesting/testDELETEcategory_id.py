import requests

# URL base del endpoint
BASE_URL = "https://effb-190-240-74-248.ngrok-free.app/categories/"

def delete_category(category_id):
    print(f"Eliminando la categoría con ID: {category_id}...")
    
    # Hacer la solicitud DELETE
    response = requests.delete(f"{BASE_URL}{category_id}")
    
    # Comprobar el estado de la respuesta
    if response.status_code == 200:
        response_json = response.json()
        print(f"Test passed: 200 ")
        print(f"Categoría eliminada: {response_json}")
    elif response.status_code == 404:
        print(f"Test failed: 404 ")
    else:
        print(f"Error: {response.status_code}")

# Prueba de eliminación
delete_category(9)  # Cambia el ID según la categoría que quieras eliminar