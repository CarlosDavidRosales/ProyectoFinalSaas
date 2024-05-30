from django import forms
from .models import *
from django.contrib.auth.hashers import make_password

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'posicion', 'contraseña']

    
class PosicionForm(forms.ModelForm):
    class Meta:
        model = Posicion
        fields = ['nombre']
        
class InventarioForm(forms.ModelForm):
    class Meta:
        model = InventarioConsumible
        fields = ['id_producto', 'id_tipo', 'nombre', 'proveedor', 'lote', 'cantidad', 'caducidad']
        widgets = {
            'caducidad': forms.DateInput(attrs={'type': 'date'}),
        }
        
class InventarioTipoForm(forms.ModelForm):
    class Meta:
        model = InventarioTipo
        fields = ['tipo']
        
class InventarioEquipoForm(forms.ModelForm):
    class Meta:
        model = InventarioEquipo
        fields = ['id_equipo', 'id_tipo', 'nombre', 'marca', 'modelo', 'Numero_serie', 'descripcion']
        
class EquipoTipoForm(forms.ModelForm):
    class Meta:
        model = EquipoTipo
        fields = ['tipo']
        
class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nombre', 'apellido', 'sexo', 'fecha_nacimiento', 'telefono', 'email', 'telefono_emergencia']

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['fecha', 'hora_inicio', 'hora_termino', 'dentista', 'paciente', 'procedimiento', 'finalizada']

class ProcedimientoForm(forms.ModelForm):
    class Meta:
        model = Procedimiento
        fields = ['nombre', 'descripcion'] 