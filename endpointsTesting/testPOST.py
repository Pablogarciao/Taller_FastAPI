import requests

# URL base del endpoint
BASE_URL = "https://effb-190-240-74-248.ngrok-free.app/categories/"

# Datos para crear la categoría (puedes modificar estos valores)
category_data = {
    "category_name": "Electronics",
    "description": "All electronics",
    "picture": ""
}

def get_total_records():
    response = requests.get(f"{BASE_URL}1")  # Obtener la primera página
    if response.status_code == 200:
        total_records = len(response.json())
        return total_records
    else:
        print(f"Error al obtener el total de registros: {response.status_code}")
        return None

def get_next_category_id():
    response = requests.get(f"{BASE_URL}1")  # Obtener la primera página de categorías
    if response.status_code == 200:
        categories = response.json()
        if categories:
            max_category_id = max(category["category_id"] for category in categories)
            return max_category_id + 1
        else:
            return 1  # Si no hay categorías, el próximo ID será 1
    else:
        print(f"Error al obtener el máximo category_id: {response.status_code}")
        return None

def create_category():
    print("Creando una nueva categoría...")

    initial_total_records = get_total_records()
    if initial_total_records is None:
        print("No se pudo obtener el número total de registros.")
        return

    next_category_id = get_next_category_id()
    if next_category_id is None:
        print("No se pudo calcular el próximo category_id.")
        return

    response = requests.post(BASE_URL, json=category_data)

    if response.status_code == 200:
        response_json = response.json()

        # Calcular el expected_total_records (total anterior + 1)
        expected_total_records = initial_total_records + 1

        expected_response = {
            "message": "Category created successfully",
            "added_records": 1,
            "total_records": expected_total_records,
            "data": {
                "category_id": next_category_id,  # Usamos el next_category_id calculado
                "category_name": category_data["category_name"],
                "description": category_data["description"],
                "picture": category_data["picture"]
            }
        }

        # Comparamos si la respuesta actual coincide con la esperada
        if response_json == expected_response:
            print("Test passed: La respuesta es correcta.")
        else:
            print("Test failed: La respuesta no coincide.")
            print(f"Respuesta esperada: {expected_response}")
            print(f"Respuesta recibida: {response_json}")

        # Imprimir todos los detalles de la categoría creada
        print("\nDetalles de la categoría creada:")
        print(f"category_id: {response_json['data']['category_id']}")
        print(f"category_name: {response_json['data']['category_name']}")
        print(f"description: {response_json['data']['description']}")
        print(f"picture: {response_json['data']['picture']}")
        print(f"Total de categorías ahora: {response_json['total_records']}")

    else:
        print(f"Error al crear la categoría: {response.status_code}")
        print(f"Respuesta: {response.json()}")

# Ejecutar la prueba
create_category()
