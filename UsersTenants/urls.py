# UserTenants/urls.py
from django.conf.urls import handler404
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('Profile/' , user_profile, name='user_profile'),
    path('Salir', Salir, name='Salir'),
    path('Profile/Crear/', Crear, name='Crear'),
    path('Profile/editar/<int:id>/', editar_empleado, name='editar_empleado'),
    path('Profile/eliminar/<int:id>/', eliminar_empleado, name='eliminar_empleado'),
    path('Posicion/', CrearPosicion, name='CrearPosicion'),
    path('Posicion/editar/<int:id>/', editar_posicion, name='editar_posicion'),
    path('Posicion/eliminar/<int:id>/', eliminar_posicion, name='eliminar_posicion'),
    path('GeneralInventario/', GeneralInventario, name='GeneralInventario'),
    path('GeneralInventario/Insumos/', Inventario, name='Inventario'),
    path('GeneralInventario/Insumos/Tipos', crear_tipo, name='Tipos Insumos'),
    path('GeneralInventario/Insumos/Editar/<int:id>/', editar_producto, name='editar_producto'),
    path('GeneralInventario/Insumos/Eliminar/<int:id>/', eliminar_producto, name='eliminar_producto'),
    path('Pacientes/', Pacientes, name='Pacientes'),
    path('Consultas/', Consultas, name='Consultas'),
    path('Reportes/', Reportes, name='Reportes'),
]

