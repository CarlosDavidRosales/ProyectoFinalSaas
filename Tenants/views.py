# Tenants/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Client, Domain
from UsersTenants.models import Empleado  # Importar el modelo Empleado desde UserTenants
from django.db import transaction
from django.http import HttpResponseRedirect
from django_tenants.utils import schema_context

def home(request):
    if request.method == "POST":
        print(request.POST)
        if request.POST['form_type'] == 'login':
            username = request.POST['username']
            password = request.POST['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                tenant = get_object_or_404(Client, clinica=user)
                domain = get_object_or_404(Domain, tenant=tenant)
                redirect_url = f"http://{domain.domain}:8000/"
                return HttpResponseRedirect(redirect_url)
            else:
                return render(request, 'home.html', {'message': 'Usuario o contraseña incorrectos'})
        elif request.POST['form_type'] == 'register':
            print(request.POST['Clinica'])
            username = request.POST['Clinica']
            password = request.POST['password']
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            telefono = request.POST['telefono']
            direccion = request.POST['direccion']
            email = str(request.POST['email']).lower()
            with transaction.atomic():
                try:
                    clinica = User.objects.create_user(username=str(username).lower(), password=password)
                    print(clinica.id)
                    
                    client = Client.objects.create(
                        clinica=clinica,
                        nombre=nombre,
                        apellido=apellido,
                        telefono=telefono,
                        direccion=direccion,
                        schema_name=username.lower()
                    )
                    
                    client.save()
                    
                    domain = Domain()
                    domain.domain = username + '.localhost'
                    domain.tenant = client
                    domain.is_primary = True
                    domain.save()
                    
                    # Cambiar al esquema del nuevo tenant
                    with schema_context(client.schema_name):
                        # Crear un registro en la tabla Empleado
                        Empleado.objects.create(
                            nombre=nombre,
                            apellido=apellido,
                            posicion='Admin',
                            usuario=username.lower(),
                            contraseña=password
                        )
                    
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        print(user.id)
                        tenant = get_object_or_404(Client, clinica_id=user.id)
                        print(tenant.id)
                        domain = get_object_or_404(Domain, tenant_id=tenant.id)
                        redirect_url = f"http://{domain.domain}:8000/"  # asegúrate que el protocolo sea correcto
                        print(redirect_url)
                        return HttpResponseRedirect(redirect_url)
                except Exception as e:
                    print(e)
                    return render(request, 'home.html', {'message': 'Ya existe la clínica y/o el usuario: ' + username})
    else:
        return render(request, 'home.html')
