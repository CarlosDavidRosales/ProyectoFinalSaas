# UsersTenants/views.py

from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from datetime import date, timedelta
from django.contrib import messages
from .models import *
from .forms import *


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
                return TemplateResponse(request, 'index.html', {"user": None, "clinica": request.tenant.nombre_clinica})
        except Empleado.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')
            return TemplateResponse(request, 'index.html', {"user": None, "clinica": request.tenant.nombre_clinica})
    else:
        if 'usuario' in request.session:
            usuario = request.session['usuario']
            try:
                user = Empleado.objects.get(usuario=usuario)
                return TemplateResponse(request, 'index.html', {"user": user, "clinica": request.tenant.nombre_clinica})
            except Empleado.DoesNotExist:
                pass
        return TemplateResponse(request, 'index.html', {"user": None, "clinica": request.tenant.nombre_clinica})
    
def user_profile(request):
    if 'usuario' not in request.session:
        return redirect('index')
    
    user_profile = Empleado.objects.get(usuario=request.session['usuario'])
    if request.method == 'POST':
        user_profile.nombre = request.POST.get('nombre')
        user_profile.apellido = request.POST.get('apellido')
        password = request.POST.get('password')
        
        if password:
            user_profile.contraseña = make_password(password)
            user_profile.save()
            
        user_profile.save()
        return redirect('user_profile')    
    return TemplateResponse(request, 'profile.html', {'user_profile': user_profile, 'posicion': str(user_profile.posicion), "clinica": request.tenant.nombre_clinica})

def Crear(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)
            last_id = Empleado.objects.latest('id_empleado').id_empleado if Empleado.objects.exists() else 0
            empleado.usuario = f"{str(empleado.nombre.lower()).replace(' ', '')[:3]}{str(empleado.apellido.lower()).replace(' ', '')[:3]}{last_id + 1}"
            if form.cleaned_data['contraseña']:
                empleado.contraseña = form.cleaned_data['contraseña']
            empleado.save()
            return redirect('Crear')
    else:
        form = EmpleadoForm()

    usuarios = Empleado.objects.all()
    return TemplateResponse(request, 'Crear.html', {
        "clinica": request.tenant.nombre_clinica,
        'form': form,
        'empleados': usuarios,
        'user_profile': Empleado.objects.get(usuario=request.session['usuario']),
        'Posicion': Posicion.objects.all(),
    })
    
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
            print(empleado.contraseña)
            form.save()
            print(empleado.contraseña)
            return redirect('Crear')
        print("NO Valido")
    else:
        form = EmpleadoForm(instance=empleado)
    
    return TemplateResponse(request, 'Editar.html', {"clinica": request.tenant.nombre_clinica, 'form': form, 'empleado': empleado, 'Posicion': Posicion.objects.all(),})

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
            return TemplateResponse(request, 'Posicion.html', {
                'Posicion': Posicion.objects.all(),
                'error': 'Error al crear el puesto',
                'user_profile': Empleado.objects.get(usuario=request.session['usuario'])
            })
        
    
    return TemplateResponse(request, 'Posicion.html', {
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
    return TemplateResponse(request, 'EditarPosicion.html', {'form': form, "clinica": request.tenant.nombre_clinica})

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
    return TemplateResponse(request, 'GeneralInventario.html', {'user_profile': Empleado.objects.get(usuario=request.session['usuario']),
                   'tipos': InventarioTipo.objects.all(),
                   'inventario': InventarioConsumible.objects.all(),
                   'equipos': InventarioEquipo.objects.all(),
                   'equipotipos': EquipoTipo.objects.all(),
                   "clinica": request.tenant.nombre_clinica}
                  )

def Equipos(request):
    if request.method == 'POST':
        form = InventarioEquipoForm(request.POST)
        if form.is_valid():
            print("VALIDO")
            form.save()
        return TemplateResponse(request, 'equipo.html', 
                  {'user_profile': Empleado.objects.get(usuario=request.session['usuario']), 
                   'form': form,
                   'equipos': InventarioEquipo.objects.all(),
                   'tipos': EquipoTipo.objects.all(),
                   "clinica": request.tenant.nombre_clinica,
                   })
    form = InventarioEquipoForm()
    return TemplateResponse(request, 'equipo.html', 
                  {'user_profile': Empleado.objects.get(usuario=request.session['usuario']), 
                   'form': form,
                   'equipos': InventarioEquipo.objects.all(),
                   'tipos': EquipoTipo.objects.all(),
                   "clinica": request.tenant.nombre_clinica
                   })

def Inventario(request):
    form = InventarioForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect('Inventario')
    
    
    return TemplateResponse(request, 'Inventario.html', 
                  {'user_profile': Empleado.objects.get(usuario=request.session['usuario']), 
                   'form': form,
                   'tipos': InventarioTipo.objects.all(),
                   'inventario': InventarioConsumible.objects.all(),
                   "clinica": request.tenant.nombre_clinica
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
            return TemplateResponse(request, 'equipotipo.html', {
                'Tipo': EquipoTipo.objects.all(),
                'error': 'Error al crear el puesto',
                'user_profile': Empleado.objects.get(usuario=request.session['usuario'])
            })
        form = EquipoTipoForm()
        return TemplateResponse(request, 'equipotipo.html', {'form': form, 'tipos':EquipoTipo.objects.all()})
    form = EquipoTipoForm()
    return TemplateResponse(request, 'equipotipo.html', {"clinica": request.tenant.nombre_clinica, 'form': form, 'tipos':EquipoTipo.objects.all()})

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
    return TemplateResponse(request, 'editarequipo.html', {'form': form, "clinica": request.tenant.nombre_clinica, 'equipo': equipo, 'tipos':EquipoTipo.objects.all()})      

@require_http_methods(["POST"])
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
    
    return TemplateResponse(request, 'EditarProducto.html', {'form': form, "clinica": request.tenant.nombre_clinica, 'producto': producto, 'tipos':InventarioTipo.objects.all()})      

@require_http_methods(["POST"])
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
            return TemplateResponse(request, 'Tipo.html', {
                'Tipo': Posicion.objects.all(),
                'error': 'Error al crear el puesto',
                'user_profile': Empleado.objects.get(usuario=request.session['usuario'])
            })
        form = InventarioTipoForm()
        return TemplateResponse(request, 'Tipo.html', {'form': form, "clinica": request.tenant.nombre_clinica, 'tipos':InventarioTipo.objects.all()})
    form = InventarioTipoForm()
    return TemplateResponse(request, 'Tipo.html', {'form': form, "clinica": request.tenant.nombre_clinica, 'tipos':InventarioTipo.objects.all()})
        

# Pacientes

def calcular_edad(fecha_nacimiento):
    hoy = date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def Pacientes(request):       
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        pas = Paciente.objects.all() 
        for paciente in pas:
            paciente.edad = calcular_edad(paciente.fecha_nacimiento)
        if form.is_valid():
            form.save()  # Ahora guarda con el usuario autogenerado
            return redirect('Pacientes')
    form = PacienteForm() # Obtener todos los usuarios
    pas = Paciente.objects.all()
    for paciente in pas:
        paciente.edad = calcular_edad(paciente.fecha_nacimiento) 
    return TemplateResponse(request, 'Paciente.html', {'form': form, "clinica": request.tenant.nombre_clinica, 'pacientes': pas, 'user_profile': Empleado.objects.get(usuario=request.session['usuario'])})



def editar_paciente(request, id):
    pas = get_object_or_404(Paciente, pk=id)
    if request.method == 'POST':  
        form = PacienteForm(request.POST, instance=pas)
        if form.is_valid():
            form.save()
            return redirect('Pacientes')
        print("NO Valido")
    else:
        form = PacienteForm(instance=pas)
    
    return TemplateResponse(request, 'EditarPaciente.html', {'form': form, "clinica": request.tenant.nombre_clinica, 'paciente': pas, 'user_profile': Empleado.objects.get(usuario=request.session['usuario'])})

@require_http_methods(["POST"])
def eliminar_paciente(request, id):
    paciente = get_object_or_404(Paciente, pk=id)
    nombre = paciente.nombre + " " + paciente.apellido
    paciente.delete()
    messages.success(request, f"Paciente: {nombre} eliminado con éxito.")
    return redirect('Pacientes')



# CONSULTAS

def Consultas(request):
    try:
        posicion = Posicion.objects.get(nombre='Dentista')
        dentistas = Empleado.objects.filter(posicion=posicion)
    except Posicion.DoesNotExist:
        dentistas = Empleado.objects.none()

    pacientes = Paciente.objects.all()
    procedimientos = Procedimiento.objects.all()
    consultas = Consulta.objects.all()

    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Consultas')
    else:
        form = ConsultaForm()

    # Manejar el perfil de usuario
    user_profile = None
    if 'usuario' in request.session:
        try:
            user_profile = Empleado.objects.get(usuario=request.session['usuario'])
        except Empleado.DoesNotExist:
            user_profile = None

    return TemplateResponse(request, 'Consulta.html', {
        'form': form,
        'consultas': consultas,
        'dentistas': dentistas,
        'pacientes': pacientes,
        'procedimientos': procedimientos,
        'user_profile': user_profile,
        "clinica": request.tenant.nombre_clinica,
    })
    
def editar_consulta(request, id):
    posicion = get_object_or_404(Posicion, nombre = 'Dentista')
    dentistas = Empleado.objects.filter(posicion = posicion.id_posicion)
    pacientes = Paciente.objects.all()
    procedimientos = Procedimiento.objects.all()
    con = get_object_or_404(Consulta, pk=id)
    if request.method == 'POST':  
        form = ConsultaForm(request.POST, instance=con)
        if form.is_valid():
            form.save()
            return redirect('Consultas')
        print("NO Valido")
    
    form = ConsultaForm(instance=con)
    return TemplateResponse(request, 'EditarConsulta.html', {'form':form, "clinica": request.tenant.nombre_clinica, 'consulta':con, 'dentistas': dentistas, 'pacientes': pacientes, 'procedimientos': procedimientos, 'user_profile': Empleado.objects.get(usuario=request.session['usuario'])})

@require_http_methods(["POST"])
def eliminar_consulta(request, id):
    con = get_object_or_404(Consulta, pk=id)
    nombre = con.id_consulta
    con.delete()
    messages.success(request, f"Consulta ID: {nombre} eliminado con éxito.")
    return redirect('Consultas')

def Procedimientos(request):
    if request.method == 'POST':
        form = ProcedimientoForm(request.POST)
        if form.is_valid():
            form.save()  # Ahora guarda con el usuario autogenerado
            return redirect('Procedimientos')  # Redirecciona a la misma vista para ver la lista actualizada
    form = ProcedimientoForm()
    return TemplateResponse(request, 'Procedimiento.html', {'form': form, "clinica": request.tenant.nombre_clinica, 'procedimientos':Procedimiento.objects.all() ,'user_profile': Empleado.objects.get(usuario=request.session['usuario']), 'Posicion': Posicion.objects.all(),})

def editar_procedimiento(request, id):
    proce = get_object_or_404(Procedimiento, pk=id)
    if request.method == 'POST':  
        form = ProcedimientoForm(request.POST, instance=proce)
        if form.is_valid():
            form.save()
            return redirect('Procedimientos')
    
    form = ProcedimientoForm(instance=proce)
    return TemplateResponse(request, 'EditarProcedimiento.html', {'form':form, "clinica": request.tenant.nombre_clinica, 'procedimiento':proce, 'user_profile': Empleado.objects.get(usuario=request.session['usuario'])})


@require_http_methods(["POST"])
def eliminar_procedimiento(request, id):
    proce = get_object_or_404(Procedimiento, pk=id)
    nombre = proce.nombre
    proce.delete()
    messages.success(request, f"Procedimiento: {nombre} eliminado con éxito.")
    return redirect('Procedimientos')

# REPORTES

def Reportes(request):
    return HttpResponse('<h1>Reportes<h1>')


# LOGIN

def Salir_tentant(request):
    request.session.flush()
    return HttpResponseRedirect("http://gestorclinicasdentales.shop")

def Salir(request):
    if 'usuario' in request.session:
        del request.session['usuario_id'] 
        del request.session['usuario'] 
        del request.session['nombre'] 
    return redirect('/')

def login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return wrapper

# Pago

def pago(request):
    if request.method == 'POST':
        # Simula el procesamiento del pago
        pagado = request.POST.get('pagado', 'true')  # Booleano, se marca como pagado

        if pagado == 'true':
            tenant = request.tenant
            tenant.pagado = True
            
            # Incrementar la fecha límite en 30 días a partir de la fecha actual
            tenant.fecha_limite = date.today() + timedelta(days=30)
            tenant.save()
            messages.success(request, 'El pago se ha realizado con éxito y los datos se han actualizado.')
            return redirect('user_profile')
        else:
            messages.error(request, 'Error en el procesamiento del pago.')

    return TemplateResponse(request, 'pago.html', {"clinica": request.tenant.nombre_clinica})
