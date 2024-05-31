from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .models import Client, Domain
from UsersTenants.models import Empleado, Posicion
from django.db import transaction
from django.http import HttpResponseRedirect
from django_tenants.utils import schema_context

def home(request):
    if request.method == "POST":
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
                
                redirect_url = f"http://{domain.domain}"
                print(redirect_url)
                return HttpResponseRedirect(redirect_url)
            else:
                return render(request, 'home.html', {'message': 'Usuario o contraseña incorrectos'})
        
        elif request.POST['form_type'] == 'register':
            username = str(request.POST['Clinica']).lower().replace(" ", "")
            nombreClinica = request.POST['Clinica']
            password = request.POST['password']
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            telefono = request.POST['telefono']
            direccion = request.POST['direccion']
            email = str(request.POST['email']).lower()
            
            # Verificación de existencia de usuario y cliente
            if User.objects.filter(username=username.lower()).exists():
                return render(request, 'home.html', {'message': 'El nombre de usuario ya existe.'})
            if Client.objects.filter(schema_name=username.lower()).exists():
                return render(request, 'home.html', {'message': 'El nombre de la clínica ya existe.'})

            with transaction.atomic():
                # Crear el usuario de la clínica
                clinica = User.objects.create_user(username=username.lower(), password=password)
                # Crear el cliente y dominio
                client = Client.objects.create(
                    clinica=clinica,
                    nombre=nombre,
                    apellido=apellido,
                    telefono=telefono,
                    direccion=direccion,
                    schema_name=username,
                    nombre_clinica=nombreClinica
                )
                domain = Domain(domain=f"{username}.gestorclinicasdentales.shop", tenant=client, is_primary=True)
                domain.save()
                
                # Crear el esquema y datos iniciales del tenant
                with schema_context(client.schema_name):
                    Posicion.objects.create(id_posicion=1, nombre='Administrador')
                    Empleado.objects.create(
                        nombre=nombre,
                        apellido=apellido,
                        posicion=get_object_or_404(Posicion, pk=1),
                        usuario=username.lower(),
                        contraseña=password
                    )
                
                # Autenticar y redirigir al usuario
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    tenant = get_object_or_404(Client, clinica_id=user.id)
                    domain = get_object_or_404(Domain, tenant_id=tenant.id)
                    redirect_url = f"http://{domain.domain}"
                    return HttpResponseRedirect(redirect_url)
                    
            return render(request, 'home.html', {'message': 'Ocurrió un error durante el registro.'})

        return render(request, 'home.html', {'message': 'Formulario no válido'})
    
    return render(request, 'home.html')
