from django import forms
from .models import Empleado, Posicion
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