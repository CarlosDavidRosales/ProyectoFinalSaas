from django.db import models
from django.contrib.auth.hashers import make_password

class Posicion(models.Model):
    id_posicion = models.IntegerField(primary_key=True)
    nombre = models.CharField()
    
    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    id_empleado = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    posicion = models.CharField(max_length=100)
    usuario = models.CharField(max_length=100, unique=True)
    contraseña = models.CharField(max_length=100)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password if the record is new
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre