"""web_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django import views     #  <<==========
from . import views     #  <<==========
from administrador import views   #  <<==========

urlpatterns = [
    path('', views.visualizar, name="index"), #  <<==========
    path('administrador/', views.login_view, name='login'), #  <<==========
    path('logout/', views.logout_view, name='logout'),
    path('Agora', views.visualizar1, name="index2"), #  <<==========
    path('listar', views.listar, name="listar"),   #  <<==========
    path('agregar', views.agregar, name="agregar"),   #  <<==========
    path('actualizar/<int:idRegistro>', views.actualizar, name="actualizar"),   #  <<==========
    path('eliminar/<int:idRegistro>', views.eliminar, name="eliminar"),   #  <<==========
]
