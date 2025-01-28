# Documentación para ejecutar la API de urls

Acontinuación se incluye el tutorial para correr el programa referente al ejercicio 2:

## 1. Clonar el repositorio
Clona el repositorio desde GitHub usando el siguiente comando:

```bash
git clone <URL_DEL_REPOSITORIO>
```
## 2. Situarse en la carpeta de la API
Cambia al directorio Ejercicio2 el cual contiene los recursos de la API:

```bash
cd Ejercicio2
```
## 3. Instalar dependencias
Utiliza el siguiente comando para instalar las dependencias necesarias:
```bash
pip install -r requirements.txt
```

## 4. Migrar la base de datos
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```

## 5. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```

## 6. Acceder a la aplicación
Accede a la API en tu navegador en 
```bash
http://127.0.0.1:8000/
```
