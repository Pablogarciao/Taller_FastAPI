# Taller FastAPI
Taller para usar una base de datos con FastAPI.


## Requisitos
Se debe trabajar en un sistema de alguna distro de linux. Como  WSL (para Windows) o Mac.

Ademas se debe tener:

- Docker instalado y abrirlo en el momento de la ejecucion del setup
- Tener python3 instalado
- Tener python3-venv instalado


## Ejecucion
Abrir la terminal sobre esta carpeta y ejecutar el siguiente comando:

```
bash setup.sh
```

Este comando hara lo siguiente:

- Creacion del Docker.
- Creacion de la base de datos "northwind" en el docker. 
- Crear un entorno virtual y librerias necesarias para el programa
- Por ultimo, ejecutará el programa

Despues de esto, se puede copiar el siguiente link en un navegador para usarlo:

```
http://localhost:8000/docs
```


## Uso
Cuenta con las siguientes rutas:

### Create Category
- **Metodo:** POST
- **Ruta:** /categories
- **Descripcion**: Crear una categoria

### Read Category
- **Metodo:** GET
- **Ruta:** /category/{category_id}
- **Descripcion**: Obtener una categoria por el id que se pase por parametro

### Read Categories
- **Metodo:** GET
- **Ruta:** /categories/{page}
- **Descripcion**: Paginación para la obtencion de categorias. Cada pagina cuenta con un maximo de 100 categorias

### Update Category
- **Metodo:** PUT
- **Ruta:** /categories/{category_id}
- **Descripcion**: Editar la categoria del id que se pase por parametro

### Delete Category
- **Metodo:** DELETE
- **Ruta:** /categories/{category_id}
- **Descripcion**: Eliminar la categoria del id que se pase por parametro

### Populate Categories
- **Metodo:** POST
- **Ruta:** /populate_categories
- **Descripcion**: Llena la tabla de categories con un total de 1000 filas