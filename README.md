# Documentación Api URLs


La API de la prueba 2 permite generar urls cortas a partir de cualquier url a la que se pueda accesar y redirigir a dicha url usando la url corta, para el desarrollo se usó el framework django
Acontinuación se incluye el tutorial para correr la API:

## Ejecutar la API
### 1. Clonar el repositorio
Clona el repositorio desde GitHub usando el siguiente comando:
```bash
git clone https://github.com/GerardoVillla/Challenge.git
```
### 2. Situarse en la carpeta de la API
Cambia al directorio Ejercicio2 el cual contiene los recursos de la API:

```bash
cd Ejercicio2
```
### 3. Instalar dependencias
Utiliza el siguiente comando para instalar las dependencias necesarias:
```bash
pip install -r requirements.txt
```

### 4. Migrar la base de datos
```bash
python manage.py migrate
```

### 5. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

### 6. Acceder a la aplicación
Accede a la API en tu navegador en 
```bash
http://127.0.0.1:8000/
```
## Endpoints
De acuerdo a los requerimientos de la prueba se presentan los servicios disponibles en la API:

### Autenticación
- **Crear usuario**: `POST /auth/register`
- Body:
```json
{
  "email": "someone@gmail.com"
  "password": "123"
}
```
- **Iniciar sesion**: `POST /auth/login`
- Body:
```json
{
  "email": "someone@gmail.com"
  "password": "123"
}
```
- **Perfil**: `POST /auth/profile`
- Body:
```json
{
  "email": "someone@gmail.com"
  "password": "123"
}
```
### Urls
Para la creación, eliminación o actualización de URLs privadas se necesita del **token de autenticación** proporcionado al iniciar sesión, de lo contrario el sistema arrojará un error de autorización.

- **Crear URL corta**: `POST /url`
- Body:
```json
{
  "original_url": "https://www.google.com"
}
```
- **Redireccionar URL**: `GET /{short_code}`
  
- **Actualizar URL**: `PATCH /url/{id}`
- Body:
```json
{
  "new_url": "https://www.amazon.com"
}
```
- **Eliminar URL**: `DELETE /url/{id}`

- **Crear urls massivamente**: `POST /url/create_massive/`
> **Nota:** Si entre la lista se encuentra una URL privada el usuario deberá enviar la solicitud con el token de autenticación de lo contrario el sistema arrojará error de permisos.
- Body:
```json
{
  "urls": [ {"original_url : ""https://www.amazon.com",
              "is_public" : true
            },
            {"original_url : ""https://www.amazon.com",
              "is_public" : false
            }
          ]
}
```

- **Listar urls (paginas de 20)**: `GET /url/list/{page}`

- **Documentación swagger**: `GET /swagger/docs/`
