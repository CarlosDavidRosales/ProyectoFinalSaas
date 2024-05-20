# UserTenants/views.py

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Empleado, Posicion
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        contraseña = request.POST.get('password')
        print(Empleado.objects.all())

        try:
            user = Empleado.objects.get(usuario=usuario)
            if contraseña == user.contraseña:
                request.session['usuario_id'] = user.id_empleado
                request.session['usuario'] = user.usuario
                request.session['nombre'] = user.nombre
                print("REGRESA")
                print(request.session['usuario'])
                return render(request, 'profile.html', {"user": user})
            else:
                print("Contraseña incorrecta")
                messages.error(request, 'Contraseña incorrecta')
                return render(request, 'index.html', {"user": None})
        except Empleado.DoesNotExist:
            print("Usuario no encontrado")
            messages.error(request, 'Usuario no encontrado')
            return render(request, 'index.html', {"user": None})
    else:
        if 'usuario' in request.session:
            usuario = request.session['usuario']
            try:
                user = Empleado.objects.get(usuario=usuario)
                return render(request, 'index.html', {"user": user})
            except Empleado.DoesNotExist:
                pass
        return render(request, 'index.html', {"user": None})

def user_profile(request):
    print(request.session['usuario'])
    user_profile = Empleado.objects.get(usuario=request.session['usuario'])
    print(user_profile.nombre)
    print(user_profile.posicion)
    print(user_profile.usuario)
    print(user_profile.apellido)
    if request.method == 'POST':
        user_profile.nombre = request.POST.get('nombre')
        user_profile.apellido = request.POST.get('apellido')
        user_profile.posicion = request.POST.get('posicion')
        user_profile.usuario = request.POST.get('usuario')
        password = request.POST.get('password')
        
        if password:
            user_profile.contraseña = password
            user_profile.save()
        
        user_profile.save()
        return redirect('user_profile')
    
    return render(request, 'profile.html', {'user_profile': user_profile})

def inventory_list(request):
    return HttpResponse("<h1>Inventory</h1>")

def staff_list(request):
    return HttpResponse("<h1>Staff</h1>")

def logout_view(request):
    request.session.flush()
    return redirect('login_view')

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('login_view')
        return view_func(request, *args, **kwargs)
    return wrapper
