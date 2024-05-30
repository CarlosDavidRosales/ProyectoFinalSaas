from django import forms
from .models import *
from django.contrib.auth.hashers import make_password

class EmpleadoForm(forms.ModelForm):
    contraseña = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = Empleado
        fields = ['nombre', 'apellido', 'posicion', 'contraseña']

    def clean_contraseña(self):
        # Obtén la contraseña que fue enviada con el formulario
        contraseña = self.cleaned_data.get('contraseña')
        # Si hay una nueva contraseña, encriptarla antes de guardarla
        if contraseña:
            return make_password(contraseña)
        # Si no hay contraseña nueva, devuelve None para indicar que no se debe cambiar
        return None
    
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