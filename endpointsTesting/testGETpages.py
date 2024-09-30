import requests

# URL base del endpoint
BASE_URL = "https://effb-190-240-74-248.ngrok-free.app/categories/"

# Página que deseas probar
page_to_test = 1  # Cambia esto según la página que quieras probar

def read_categories():
    print(f"Buscando categorías en la página: {page_to_test}...")

    # Hacer la solicitud GET
    response = requests.get(f"{BASE_URL}{page_to_test}")

    if response.status_code == 200:
        response_json = response.json()

        # Verificar si la lista está vacía
        if not response_json:
            print(f"No hay categorías en la página {page_to_test}.")
            return

        # Categoría esperada (puedes cambiarlo por cualquier otra)
        expected_category_name = "Electronics"
        
        # Recorrer la lista y verificar si existe la categoría esperada
        category_found = False
        for category in response_json:
            if category["category_name"] == expected_category_name:
                category_found = True
                break

        # Verificar si se encontró la categoría
        if category_found:
            print(f"Test passed: La categoría '{expected_category_name}' está presente.")
        else:
            print("Test failed: La categoría no coincide.")
            print(f"Respuesta esperada: {expected_category_name}")
            print(f"Respuesta recibida: {[cat['category_name'] for cat in response_json]}")
    
    elif response.status_code == 400:
        print("Test failed: La página debe ser >= 1.")
    else:
        print(f"Error al buscar las categorías: {response.status_code}")
        print(f"Respuesta: {response.json()}")

# Ejecutar la prueba
read_categories()
