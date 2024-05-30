# UsersTenants/views.py

from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from .models import *
from .forms import *

print(make_password('Carlos'))

def verificar_contraseña(empleado, contraseña):
    if check_password(contraseña, empleado.contraseña):
        return True
    return False

# USUARIOS

def index(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        contraseña = request.POST.get('password')
        try:
            user = Empleado.objects.get(usuario=usuario)
            
            if check_password(contraseña, user.contraseña):
                request.session['usuario_id'] = user.id_empleado
                request.session['usuario'] = user.usuario
                request.session['nombre'] = user.nombre
                return redirect('user_profile')
            else:
                messages.error(request, 'Contraseña incorrecta')
                return render(request, 'index.html', {"user": None})
        except Empleado.DoesNotExist:
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
    if 'usuario' not in request.session:
        return redirect('index')
    
    user_profile = Empleado.objects.get(usuario=request.session['usuario'])
    print(len(str(user_profile.posicion)))
    if request.method == 'POST':
        user_profile.nombre = request.POST.get('nombre')
        user_profile.apellido = request.POST.get('apellido')
        password = request.POST.get('password')
        
        if password:
            user_profile.contraseña = make_password(password)
            user_profile.save()
            
        user_profile.save()
        return redirect('user_profile')    
    return render(request, 'profile.html', {'user_profile': user_profile, 'posicion': str(user_profile.posicion)})

def Crear(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)  # No guardes todavía
            # Autogenerar el nombre de usuario
            last_id = Empleado.objects.latest('id_empleado').id_empleado if Empleado.objects.exists() else 0
            empleado.usuario = f"{ str(empleado.nombre.lower()).replace(' ', '')[:3] }{ str(empleado.apellido.lower()).replace(' ', '')[:3] }{last_id + 1}"
            empleado.save()  # Ahora guarda con el usuario autogenerado
            return redirect('Crear')  # Redirecciona a la misma vista para ver la lista actualizada
    form = EmpleadoForm()
    usuarios = Empleado.objects.all()  # Obtener todos los usuarios
    return render(request, 'Crear.html', {'form': form, 'empleados': usuarios, 'user_profile': Empleado.objects.get(usuario=request.session['usuario']), 'Posicion': Posicion.objects.all(),})

def editar_empleado(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    if request.method == 'POST':        
        posicion_actual = str(empleado.posicion)
        print(request.POST)
        form = EmpleadoForm(request.POST, instance=empleado)
        if not request.POST.get('contraseña'):  # Verifica si el campo de contraseña está vacío
            del form.fields['contraseña']  # Elimina el campo de contraseña del formulario para evitar la validación
        
        if form.is_valid():
            if posicion_actual == 'Administrador':
                posicion = get_object_or_404(Posicion, nombre = 'Administrador')
                num_admins = Empleado.objects.filter(posicion=posicion.id_posicion).count()
                print(num_admins)
                if num_admins <= 1:
                    messages.error(request, "No se puede cambiar de posicion al último administrador.")
                    return redirect('Crear') 
                
            #Guarda el formulario pero maneja la contraseña de forma especial
            empleado = form.save(commit=False)
            nueva_contraseña = form.cleaned_data.get('contraseña')
            if nueva_contraseña is not None:
               empleado.contraseña = nueva_contraseña
            empleado.save()
            return redirect('Crear')
        print("NO Valido")
    else:
        form = EmpleadoForm(instance=empleado)
    
    return render(request, 'Editar.html', {'form': form, 'empleado': empleado, 'Posicion': Posicion.objects.all(),})

@require_http_methods(["POST"])
def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    usuario = empleado.usuario
    if str(empleado.posicion) == 'Administrador':
        posicion = get_object_or_404(Posicion, nombre = 'Administrador')
        num_admins = Empleado.objects.filter(posicion=posicion.id_posicion).count()
        if num_admins <= 1:
            messages.error(request, "No se puede eliminar al último administrador.")
            return redirect('Crear')  # Suponiendo que 'lista_empleados' es tu URL para la lista de empleados
    
    # Si no es el último admin, procede con la eliminación
    empleado.delete()
    messages.success(request, f"Empleado: {usuario} eliminado con éxito.")
    return redirect('Crear')

# POSICIONES
def CrearPosicion(request):
    if request.method == 'POST':
        nombre_puesto = request.POST['nombre_puesto']   
        nombre_puesto = nombre_puesto.capitalize()
        if Posicion.objects.filter(nombre = nombre_puesto).exists():
            messages.error(request, f'La posicion {nombre_puesto} ya existe')
            return redirect('CrearPosicion')
        
        try:
            Posicion.objects.create(
                id_posicion = Posicion.objects.count() + 1,
                nombre = nombre_puesto
            )
        except Exception as e:
            print(e)
            return render(request, 'Posicion.html', {
                'Posicion': Posicion.objects.all(),
                'error': 'Error al crear el puesto',
                'user_profile': Empleado.objects.get(usuario=request.session['usuario'])
            })
        
    
    return render(request, 'Posicion.html', {
        'Posicion': Posicion.objects.all(),
        'user_profile': Empleado.objects.get(usuario=request.session['usuario'])
    })

def editar_posicion(request, id):
    posicion = get_object_or_404(Posicion, pk=id)
    if request.method == 'POST':
        form = PosicionForm(request.POST, instance=posicion)
        if form.is_valid():
            print("Valido")
            posicion = form.save()
            return redirect('CrearPosicion')
        print("NO Valido")
    else:
        form = PosicionForm(instance=posicion)
    return render(request, 'EditarPosicion.html', {'form': form})

@require_http_methods(["POST"])
def eliminar_posicion(request, id):
    posicion = get_object_or_404(Posicion, pk=id)
    nombre = posicion.nombre
    if posicion.nombre == 'Administrador':
        messages.error(request, "No se puede eliminar la posicion administrador.")
        return redirect('CrearPosicion') 
    
    # Si no es el último admin, procede con la eliminación
    posicion.delete()
    messages.success(request, f"Posicion: {nombre} eliminada con éxito.")
    return redirect('CrearPosicion')

# INVENTARIOS

def GeneralInventario(request):
    return render(request, 'GeneralInventario.html', {'user_profile': Empleado.objects.get(usuario=request.session['usuario']),
                   'tipos': InventarioTipo.objects.all(),
                   'inventario': InventarioConsumible.objects.all(),
                   'equipos': InventarioEquipo.objects.all(),
                   'equipotipos': EquipoTipo.objects.all(),
                   })

def Equipos(request):
    if request.method == 'POST':
        form = InventarioEquipoForm(request.POST)
        if form.is_valid():
            print("VALIDO")
            form.save()
        return render(request, 'equipo.html', 
                  {'user_profile': Empleado.objects.get(usuario=request.session['usuario']), 
                   'form': form,
                   'equipos': InventarioEquipo.objects.all(),
                   'tipos': EquipoTipo.objects.all(),
                   })
    form = InventarioEquipoForm()
    return render(request, 'equipo.html', 
                  {'user_profile': Empleado.objects.get(usuario=request.session['usuario']), 
                   'form': form,
                   'equipos': InventarioEquipo.objects.all(),
                   'tipos': EquipoTipo.objects.all(),
                   })

def Inventario(request):
    form = InventarioForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect('Inventario')
    
    
    return render(request, 'Inventario.html', 
                  {'user_profile': Empleado.objects.get(usuario=request.session['usuario']), 
                   'form': form,
                   'tipos': InventarioTipo.objects.all(),
                   'inventario': InventarioConsumible.objects.all(),
                   })


def crear_tipo_equipo(request):
    if request.method == 'POST':
        tipo = request.POST['tipo']
        tipo = tipo.capitalize()
        
        if EquipoTipo.objects.filter(tipo = tipo).exists():
            print(f'El tipo {tipo} ya existe')
            messages.error(request, f'El tipo {tipo} yaa existe')
            return redirect('crear_tipo')
        
        try:
            EquipoTipo.objects.create(
                id_tipo = EquipoTipo.objects.count() + 1,
                tipo = tipo
            )
        except Exception as e:
            print(e)
            return render(request, 'equipotipo.html', {
                'Tipo': EquipoTipo.objects.all(),
                'error': 'Error al crear el puesto',
                'user_profile': Empleado.objects.get(usuario=request.session['usuario'])
            })
        form = EquipoTipoForm()
        return render(request, 'equipotipo.html', {'form': form, 'tipos':EquipoTipo.objects.all()})
    form = EquipoTipoForm()
    return render(request, 'equipotipo.html', {'form': form, 'tipos':EquipoTipo.objects.all()})

def editar_equipo(request, id):
    equipo = get_object_or_404(InventarioEquipo, pk = id)
    if request.method == 'POST':
        form = InventarioEquipoForm(request.POST, instance = equipo)
        if form.is_valid():
            print("VALIDO")
            for field in form.cleaned_data:
                if form.cleaned_data[field] is None:
                    setattr(equipo, field, form.cleaned_data[field])
            equipo.save()
            return redirect('Equipos')
    
    form = InventarioEquipoForm(instance=equipo)
    return render(request, 'editarequipo.html', {'form': form, 'equipo': equipo, 'tipos':EquipoTipo.objects.all()})      

def eliminar_equipo(request, id):
    equipo = get_object_or_404(InventarioEquipo, pk=id)
    nombre = equipo.nombre
    equipo.delete()
    messages.success(request, f"Producto: {nombre} eliminado con éxito.")
    return redirect('Equipos')


def editar_producto(request, id):
    producto = get_object_or_404(InventarioConsumible, pk = id)
    if request.method == 'POST':
        form = InventarioForm(request.POST, instance = producto)
        if not request.POST.get('caducidad'):  # Verifica si el campo de contraseña está vacío
            del form.fields['caducidad']
        if form.is_valid():
            print("VALIDO")
            for field in form.cleaned_data:
                if form.cleaned_data[field] is None:
                    setattr(producto, field, form.cleaned_data[field])
            producto.save()
            return redirect('Inventario')
    else:
        form = InventarioForm(instance = producto)
    
    return render(request, 'EditarProducto.html', {'form': form, 'producto': producto, 'tipos':InventarioTipo.objects.all()})      

def eliminar_producto(request, id):
    producto = get_object_or_404(InventarioConsumible, pk=id)
    nombre = producto.nombre
    producto.delete()
    messages.success(request, f"Producto: {nombre} eliminado con éxito.")
    return redirect('Inventario')

def crear_tipo(request):
    if request.method == 'POST':
        tipo = request.POST['tipo']
        tipo = tipo.capitalize()
        
        if InventarioTipo.objects.filter(tipo = tipo).exists():
            print(f'El tipo {tipo} ya existe')
            messages.error(request, f'El tipo {tipo} yaa existe')
            return redirect('crear_tipo')
        
        try:
            InventarioTipo.objects.create(
                id_tipo = InventarioTipo.objects.count() + 1,
                tipo = tipo
            )
        except Exception as e:
            print(e)
            return render(request, 'Tipo.html', {
                'Tipo': Posicion.objects.all(),
                'error': 'Error al crear el puesto',
                'user_profile': Empleado.objects.get(usuario=request.session['usuario'])
            })
        form = InventarioTipoForm()
        return render(request, 'Tipo.html', {'form': form, 'tipos':InventarioTipo.objects.all()})
    form = InventarioTipoForm()
    return render(request, 'Tipo.html', {'form': form, 'tipos':InventarioTipo.objects.all()})
        

# Pacientes


def Pacientes(request):
    return HttpResponse('<h1>Pacientes<h1>')


# CONSULTAS

def Consultas(request):
    return HttpResponse('<h1>Consultas<h1>')


# REPORTES

def Reportes(request):
    return HttpResponse('<h1>Reportes<h1>')


# LOGIN

def Salir(request):
    request.session.flush()
    return redirect('index')

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper

def handle_not_found(request, exception=None):
    return redirect('user_profile')  # Redirige a la URL de inicio, ajusta según sea necesario