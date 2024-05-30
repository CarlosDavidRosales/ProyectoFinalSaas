# Tenants/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Client, Domain
from UsersTenants.models import Empleado, Posicion  # Importar el modelo Empleado desde UserTenants
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django_tenants.utils import schema_context

def home(request):
    if request.method == "POST":
        print(request.POST)
        if 'form_type' not in request.POST:
            return render(request, 'home.html', {'message': 'Formulario no válido'})

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
            username = str(request.POST['Clinica']).lower().replace(" ", "")
            nombreClinica = request.POST['Clinica']
            password = request.POST['password']
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            telefono = request.POST['telefono']
            direccion = request.POST['direccion']
            email = str(request.POST['email']).lower()
            
            # Verificar si el nombre de usuario o la clínica ya existen
            if User.objects.filter(username=username.lower()).exists():
                return render(request, 'home.html', {'message': 'El nombre de usuario ya existe.'})
            if Client.objects.filter(schema_name=username.lower()).exists():
                return render(request, 'home.html', {'message': 'El nombre de la clínica ya existe.'})

            with transaction.atomic():
                clinica = User.objects.create_user(username=str(username).lower(), password=password)
                print(clinica.id)
                
                client = Client.objects.create(
                    clinica=clinica,
                    nombre=nombre,
                    apellido=apellido,
                    telefono=telefono,
                    direccion=direccion,
                    schema_name=username,
                    nombre_clinica = nombreClinica
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
                    Posicion.objects.create(
                        id_posicion = 1,
                        nombre= 'Administrador'
                    )
                    
                    Empleado.objects.create(
                        nombre=nombre,
                        apellido=apellido,
                        posicion = get_object_or_404(Posicion, pk=1),
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
                    
            # Asegurarse de devolver una respuesta en caso de que no entre en el bloque try
            return render(request, 'home.html', {'message': 'Ocurrió un error durante el registro.'})
        
        # Devolver una respuesta en caso de que no se reconozca el form_type
        return render(request, 'home.html', {'message': 'Formulario no válido'})
    else:
        return render(request, 'home.html')
    



