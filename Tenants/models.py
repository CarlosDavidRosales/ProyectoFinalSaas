from django.db import models
from django.contrib.auth.models import User
from django_tenants.models import TenantMixin, DomainMixin
# Create your models here.

class Client(TenantMixin):
    clinica = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)
    plan = models.IntegerField(default=0)
    created_on = models.DateField(auto_now_add=True)

class Domain(DomainMixin):
    pass

