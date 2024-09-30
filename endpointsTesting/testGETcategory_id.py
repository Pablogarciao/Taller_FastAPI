import requests

# URL base del endpoint
BASE_URL = "http://localhost:8000/category/"

# ID de la categoría que deseas buscar
category_id_to_test = 9  # Cambia este valor según el ID que deseas probar

def read_category():
    print(f"Buscando la categoría con ID: {category_id_to_test}...")

    # Hacer la solicitud GET
    response = requests.get(f"{BASE_URL}{category_id_to_test}")

    if response.status_code == 200:
        response_json = response.json()

        # Aquí puedes definir lo que esperas encontrar. Cambia esto según tus datos
        expected_response = {
            "category_id": category_id_to_test,
            "category_name": "Electronics",  # Cambia según el nombre esperado
            "description": "All electronics",  # Cambia según la descripción esperada
            "picture": None  # Cambia según la imagen esperada
        }

        # Comparar la respuesta recibida con la esperada
        if response_json == expected_response:
            print("Test passed: La respuesta es correcta.")
        else:
            print("Test failed: La respuesta no coincide.")
            print(f"Respuesta esperada: {expected_response}")
            print(f"Respuesta recibida: {response_json}")

    elif response.status_code == 404:
        print("Test failed: La categoría no fue encontrada.")
    else:
        print(f"Error al buscar la categoría: {response.status_code}")
        print(f"Respuesta: {response.json()}")

# Ejecutar la prueba
read_category()
