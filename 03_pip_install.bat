rem  la palabra rem es comentario
rem los que estan con rem es por que no es necesario ejecutarlos

pip install django
pip install Pillow
cd web_admin

rem  Ya existe el proyecto
rem django-admin startproject web_admin
rem cd web_admin

rem  Ya se existe la app
rem python manage.py startapp administrador
rem agregamos nuestra app al setting de nuestro proyecto

python manage.py makemigrations
python manage.py migrate

rem ya existe el super usuario (harrys/macarena)
rem python manage.py createsuperuser

python  manage.py runserver 0.0.0.0:8010

rem   http://localhost:8010/
rem   http://localhost:8010/admin