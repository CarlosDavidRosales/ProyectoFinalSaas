from django.db import models

class Posicion(models.Model):
    id_posicion = models.IntegerField(primary_key=True)
    nombre = models.CharField()
    
    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    id_empleado = models.IntegerField(primary_key=True)
    nombre = models.CharField()
    apellido = models.CharField()
    posicion = models.CharField()
    usuario = models.CharField()
    contraseña = models.CharField()
    
    def __str__(self):
        return self.nombre
