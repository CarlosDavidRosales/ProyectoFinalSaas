from django.contrib import admin
from .models import Client

# Register your models here.
@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display=(['clinica', 'nombre', 'apellido', 'telefono', 'direccion', 'plan', 'created_on'])
    search_fields=(['clinica'])