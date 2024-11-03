# Taller FastAPI
Taller para usar una base de datos con FastAPI.


## Requisitos
Se debe trabajar en un sistema de alguna distro de linux. Como  WSL (para Windows) o Mac.

Ademas se debe tener:

- Docker instalado y corriendo
- Tener python3 instalado
- Tener python3-venv instalado
- [Opcional] Tener Ngrok descargado y configurado


## Ejecucion
Abrir la terminal sobre esta carpeta y ejecutar el siguiente comando para instalar lo necesario para la ejecución:

```
bash run.sh setup
```

Este comando hara lo siguiente:

- Creacion del Docker.
- Creacion de la base de datos "northwind" en el docker. 
- Crear un entorno virtual y librerias necesarias para el programa

Despues de esto, se daran las siguientes opciones:

---
### Modo dev
Ejecutara el proyecto en modo desarrollo, se actualizara automaticamente de manera local.

**Ejecutar con:**

```
bash run.sh dev
```

Se podra usar con la siguiente URL:

```
http://localhost:8000/docs
```

---
### Modo producción
Creara un servicio para que con tener wsl y docker corriendo, se pueda usar.

**Ejecutar con:**

```
bash run.sh start
```

Se podra usar con la siguiente URL:

```
http://localhost:8000/docs
```

##### NGROK
Al levantar en produccion se da la opción de levantar este servicio de manera que cualquier persona externa pueda usarlo.

La URL puede cambiar cada que se levante, sera como el siguiente ejemplo:

```
https://1b3b-190-240-74-248.ngrok-free.app/docs
```

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Taller WSL
### Usar como instancia de ec2
Despues de tener clonado el repositorio, se debe ejecutar los siguientes comandso para tener todo listo en la instancia de ec2:
1. Conexión a la instancia

```
ssh -i "ruta hasta donde se tenga la llave.pem ec2-user@"IP Pública de la instancia EC2"
```
2. se instalan todo lo necesario dentro de la instancia de EC2 para poderla correr correctamente
```
sudo yum update -y
sudo yum install git -y
sudo yum install python3 -y
sudo yum install python3-pip -y
sudo yum install docker -y
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user
```
3. Se clona el repositorio dentro de la instancia
```
git clone URL del repositorio
```
3. Se navega hacia el repositorio
```
cd nombre de la carpeta del repositorio
```

4. Despues de tener todo levantado, usar el siguiente comando para habilitar el puerto 8000 y que sea accesible con la url publica del ec2:

```
bash run.sh ec2
```

5. Probar el correcto funcionamiento del swagger de FastAPI dentro de la instancia, pegar en el buscador web:
"IP Pública de la instancia:8000"


----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Rutas
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
- **Descripcion**: Llena la tabla de categories hasta un total de 1000 filas
