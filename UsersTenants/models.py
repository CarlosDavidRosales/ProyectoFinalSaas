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
    posicion = models.ForeignKey(Posicion, on_delete=models.SET_NULL, null=True)
    usuario = models.CharField(max_length=100, unique=True)
    contraseña = models.CharField(max_length=100)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Only hash the password if the record is new
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nombre

class InventarioTipo(models.Model):
    id_tipo = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=100)
    
    def __str__(self):
        return self.tipo    

class InventarioConsumible(models.Model):
    id_producto = models.AutoField(primary_key=True)
    id_tipo = models.ForeignKey(InventarioTipo, on_delete=models.SET_DEFAULT, default='Sin Tipo')
    nombre = models.CharField(max_length=150)
    proveedor = models.CharField(max_length=150)
    lote = models.IntegerField()
    cantidad = models.IntegerField(default=0)
    caducidad = models.DateField()