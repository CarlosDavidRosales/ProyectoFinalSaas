# UserTenants/urls.py
from django.conf.urls import handler404
from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('Profile/', user_profile, name='user_profile'),
    path('Salir', Salir, name='Salir'),
    path('TSalir', Salir_tentant, name='Salir_tentant'),
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
    path('GeneralInventario/Equipos/', Equipos, name='Equipos'),
    path('GeneralInventario/Equipos/Tipos', crear_tipo_equipo, name='crear_tipo_equipo'),
    path('GeneralInventario/Equipos/Editar/<int:id>/', editar_equipo, name='editar_equipo'),
    path('GeneralInventario/Equipos/Eliminar/<int:id>/', eliminar_equipo, name='eliminar_equipo'),
    path('Pacientes/', Pacientes, name='Pacientes'),
    path('Pacientes/Editar/<int:id>', editar_paciente, name='editar_paciente'),
    path('Pacientes/Eliminar/<int:id>', eliminar_paciente, name='eliminar_paciente'),
    path('Consultas/', Consultas, name='Consultas'),
    path('Consultas/Editar/<int:id>', editar_consulta, name='editar_consulta'),
    path('Consultas/Eliminar/<int:id>', eliminar_consulta, name='eliminar_consulta'),    
    path('Consultas/Procedimientos/', Procedimientos, name='Procedimientos'),
    path('Consultas/Procedimientos/Editar/<int:id>/', editar_procedimiento, name='editar_procedimiento'),
    path('Consultas/Procedimientos/Eliminar/<int:id>/', eliminar_procedimiento, name='eliminar_procedimiento'),
    path('Reportes/', Reportes, name='Reportes'),
    path('Pago/', pago, name='pago'),
]

