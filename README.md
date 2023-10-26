Proyecto realizado en **DJANGO v4.2**, empleando la última versión de **Python (3.12.0)**.

La base de datos a utilizar puede ser SQLite o PostgreSQL. En el desarrollo se empleó esta última. 

Para el caso de Postgres es necesario instalar la última versión disponible y configurar las variables de entorno 
según sea necesario. SQLite no require mayor configuración, la misma aplicación crea el fichero de base de datos al 
iniciar por primera vez.


# Pasos en desarrollo #

1. Instalar Python y Django en las version mencionadas.
2. Actualizar pip, emplenado comando:

```
python -m pip install -U pip
```

3. Instalar pipenv de forma global.
4. Ejecutar en la carpeta raíz del proyecto:

```
pipenv install
```

5. Una vez terminada la instalación de dependencias, ejecutar:

```
pipenv shell
```

6. Dentro de la consola del entorno virtual, ejecutar los siguientes comandos en orden:

```
python manage.py migrate
python manage.py seed
python manage.py runserver
```

7. Con el último paso la aplicación se podrá acceder en el navegador en su ruta por defecto http://localhost:8000.
8. El comando seed genera automaticamente el control de autentificación, carga los libros a la base de datos y crea al usuario
super administrador con las siguientes credenciales:

- Correo: admin@admin.cl
- Password: 1

9. Las rutas de acceso corresponden a:

- http://localhost:8000/admin -> Para acceder a la consola de administración de Django.
- http://localhost:8000/api/graphql -> Playground de la API.

