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
    posicion = models.ForeignKey('Posicion', on_delete=models.SET_NULL, null=True)
    usuario = models.CharField(max_length=100, unique=True)
    contraseña = models.CharField(max_length=128)  # Longitud suficiente para hashes

    def save(self, *args, **kwargs):
        # Hash the password only if it's new or has been changed
        if not self.pk or 'contraseña' in self.get_dirty_fields():
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    def get_dirty_fields(self):
        """Returns a dictionary of modified model fields and their original values."""
        old_values = {}
        if not self.pk:
            return old_values

        current_instance = type(self).objects.get(pk=self.pk)
        for field in self._meta.fields:
            field_name = field.name
            old_value = getattr(current_instance, field_name)
            new_value = getattr(self, field_name)
            if old_value != new_value:
                old_values[field_name] = old_value
        return old_values
    
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
    
class EquipoTipo(models.Model):
    id_tipo = models.IntegerField(primary_key=True)
    tipo = models.CharField(max_length=100)
    
    def __str__(self):
        return self.tipo  

class InventarioEquipo(models.Model):
    id_equipo = models.AutoField(primary_key=True)
    id_tipo = models.ForeignKey(EquipoTipo, on_delete=models.SET_DEFAULT, default='Sin Tipo')
    nombre = models.CharField(max_length=150)
    marca = models.CharField(max_length=150)
    modelo = models.CharField(max_length=150)
    Numero_serie = models.IntegerField()
    descripcion = models.CharField(max_length=200)
    
class Paciente(models.Model):
    id_paciente = models.AutoField(primary_key=True)
    nombre = models.CharField()
    apellido = models.CharField()
    sexo = models.CharField()
    fecha_nacimiento = models.DateField()
    telefono = models.CharField()
    email = models.EmailField()
    telefono_emergencia = models.CharField()
    
    def __str__(self):
        return f'{self.nombre} {self.apellido}'
    

class Procedimiento(models.Model):
    id_procedimiento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class Consulta(models.Model):
    id_consulta = models.AutoField(primary_key=True)
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_termino = models.TimeField()
    dentista = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)
    paciente = models.ForeignKey(Paciente, on_delete=models.SET_NULL, null=True)
    procedimiento = models.ForeignKey(Procedimiento, on_delete=models.SET_NULL, null=True)
    finalizada = models.CharField()
