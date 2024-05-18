from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from Tenants.models import Client, Domain
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from Tenants.models import Client, Domain

def home(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(user.id)
            tenant = get_object_or_404(Client, clinica_id = user.id)
            print(tenant.id)
            domain = get_object_or_404(Domain, tenant_id = tenant.id)
            redirect_url = f"http://{domain.domain}:8000/"  # asegúrate que el protocolo sea correcto
            print(redirect_url)
            return HttpResponseRedirect(redirect_url)
        else:
            print("No autenticado")
            return render(request, 'base.html', {'message': 'Usuario o contraseña incorrectos'})
    else:
        return render(request, 'base.html')
    
def register(request):
    if request.method == "POST":
            username = str(request.POST['Clinica']).lower()
            password = request.POST['password']
            nombre = request.POST['nombre']
            apellido = request.POST['apellido']
            telefono = request.POST['telefono']
            direccion = request.POST['direccion']
            email = str(request.POST['email']).lower()
            with transaction.atomic():
                try:
                    clinica = User.objects.create_user(username=username, password=password)
                    print(clinica.id)
                    
                    client = Client.objects.create(
                        clinica=clinica,
                        nombre=nombre,
                        apellido=apellido,
                        telefono=telefono,
                        direccion=direccion,
                        schema_name = username.lower()
                    )
                    
                    client.save()
                    
                    domain = Domain()
                    domain.domain = username + '.localhost'
                    domain.tenant = client
                    domain.is_primary = True
                    domain.save()
                    
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                        login(request, user)
                        print(user.id)
                        tenant = get_object_or_404(Client, clinica_id = user.id)
                        print(tenant.id)
                        domain = get_object_or_404(Domain, tenant_id = tenant.id)
                        redirect_url = f"http://{domain.domain}:8000/"  # asegúrate que el protocolo sea correcto
                        print(redirect_url)
                        return HttpResponseRedirect(redirect_url)
                    else:
                        print("No autenticado")
                        return render(request, 'base.html', {'message': 'Usuario o contraseña incorrectos'})# Redirige a una vista específica
                except Exception as e:
                    print(e)
                    return render(request, 'register.html', {'message': 'Error al crear el usuario: ' + str(username) })
    else:
        return render(request, 'register.html')  # Redirige a una vista específica
