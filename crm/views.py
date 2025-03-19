from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.db.models import Q, Sum
from datetime import date
from .models import Cliente, Vehiculo, Servicio, CatalogoServicio, ModuloReparacion, Venta
from .forms import ClienteForm, VehiculoForm, ServicioForm, CatalogoServicioForm, ModuloReparacionForm

# Menu Principal
def menu_principal(request):
    return render(request, 'crm/menu.html')

# 🔹 Vistas para Clientes
def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'crm/listar_clientes.html', {'clientes': clientes})

def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'crm/cliente_form.html', {'form': form})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'crm/cliente_form.html', {'form': form})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')
    return render(request, 'crm/confirmar_eliminar.html', {'objeto': cliente})

# 🔹 Vistas para Vehículos
def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.all()
    return render(request, 'crm/listar_vehiculos.html', {'vehiculos': vehiculos})

def registrar_vehiculo(request):
    if request.method == 'POST':
        form = VehiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_vehiculos')
    else:
        form = VehiculoForm()
    return render(request, 'crm/vehiculo_form.html', {'form': form})

def editar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        form = VehiculoForm(request.POST, instance=vehiculo)
        if form.is_valid():
            form.save()
            return redirect('listar_vehiculos')
    else:
        form = VehiculoForm(instance=vehiculo)
    return render(request, 'crm/vehiculo_form.html', {'form': form, 'vehiculo': vehiculo})

def eliminar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('listar_vehiculos')
    return render(request, 'crm/confirmar_eliminar.html', {'objeto': vehiculo})

# 🔹 Vista para obtener vehículos por cliente (para AJAX)
def obtener_vehiculos_por_cliente(request, cliente_id):
    vehiculos = Vehiculo.objects.filter(cliente_id=cliente_id).values('id', 'marca', 'modelo', 'anio')
    return JsonResponse(list(vehiculos), safe=False)

# 🔹 Vistas para Catálogo de Servicios
def listar_servicios(request):
    servicios = CatalogoServicio.objects.all()
    return render(request, 'crm/listar_servicios.html', {'servicios': servicios})

def registrar_servicio(request):
    if request.method == "POST":
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_servicios')
    else:
        form = ServicioForm()

    return render(request, 'crm/servicio_form.html', {'form': form})
# 🔹 Vistas para Registro de Servicios
def listar_servicios_registrados(request):
    servicios = Servicio.objects.all()
    return render(request, 'crm/listar_servicios_registrados.html', {'servicios': servicios})

def registrar_servicio_cliente(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_servicios_registrados')
    else:
        form = ServicioForm()
    return render(request, 'crm/servicio_cliente_form.html', {'form': form})

# 🔹 Vista para Registrar una Reparación de Módulo
def registrar_reparacion(request):
    if request.method == 'POST':
        form = ModuloReparacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_reparaciones')
    else:
        form = ModuloReparacionForm()
    return render(request, 'crm/modulo_form.html', {'form': form})

# Listar Servicios
def listar_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'crm/listar_servicios.html', {'servicios': servicios})

# Registrar Servicio
def registrar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_servicios')
    else:
        form = ServicioForm()
    return render(request, 'crm/servicio_form.html', {'form': form})

# Listar Catálogo de Servicios
def listar_catalogo_servicios(request):
    catalogo_servicios = CatalogoServicio.objects.all()
    return render(request, 'crm/listar_catalogo_servicios.html', {'catalogo_servicios': catalogo_servicios})

# Registrar Servicio en el Catálogo
def registrar_catalogo_servicio(request):
    if request.method == 'POST':
        form = CatalogoServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_catalogo_servicios')
    else:
        form = CatalogoServicioForm()
    return render(request, 'crm/catalogo_servicio_form.html', {'form': form})

# Listar Reparaciones
def listar_reparaciones(request):
    reparaciones = ModuloReparacion.objects.all()
    return render(request, 'crm/listar_reparaciones.html', {'reparaciones': reparaciones})

# Registrar Reparación de Módulo
def registrar_reparacion(request):
    cliente_id = request.GET.get('cliente', None)
    cliente = Cliente.objects.filter(id=cliente_id).first() if cliente_id else None

    if request.method == "POST":
        form = ModuloReparacionForm(request.POST)
        if form.is_valid():
            reparacion = form.save()  # Guardar la reparación en la BD

            # 🔹 Obtener el servicio "Reparacion Modulos Airbag" del catálogo
            tipo_servicio = CatalogoServicio.objects.filter(nombre_servicio="Reparacion Modulos Airbag").first()

            # 🔹 Crear el registro de servicio automáticamente
            if tipo_servicio:
                Servicio.objects.create(
                    cliente=reparacion.cliente,
                    vehiculo=None,  # No se asocia un vehículo
                    tipo_servicio=tipo_servicio,
                    precio_final=reparacion.precio_reparacion
                )

            return redirect('listar_servicios')  # Redirigir a lista de servicios
    else:
        form = ModuloReparacionForm(initial={'cliente': cliente})

    return render(request, 'crm/reparacion_form.html', {'form': form})

# Vista Ventas
def listar_ventas(request):
    ventas = Servicio.objects.all()
    return render(request, 'crm/listar_ventas.html', {'ventas': ventas })

# Reporte de Ventas

from django.http import JsonResponse
import json

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Sum
import json
from .models import Cliente, Servicio

def reporte_ventas(request):
    clientes = Cliente.objects.all()

    ventas_por_servicio = Servicio.objects.values('tipo_servicio__nombre_servicio') \
        .annotate(total=Sum('precio_final'))

    # ✅ Convertir Decimal a float antes de pasarlo a JSON
    ventas_por_servicio = [
        {"tipo_servicio__nombre_servicio": item["tipo_servicio__nombre_servicio"], "total": float(item["total"])}
        for item in ventas_por_servicio
    ]

    return render(request, 'crm/reporte_ventas.html', {
        'clientes': clientes,
        'ventas_por_servicio_json': json.dumps(ventas_por_servicio)
    })

# Nueva vista para filtrar ventas por cliente
def ventas_por_cliente(request):
    cliente_id = request.GET.get('cliente_id')
    if cliente_id:
        ventas = Servicio.objects.filter(cliente_id=cliente_id).values('tipo_servicio__nombre_servicio') \
            .annotate(total=Sum('precio_final'))
    else:
        ventas = Servicio.objects.values('tipo_servicio__nombre_servicio') \
            .annotate(total=Sum('precio_final'))

    ventas = [{"tipo_servicio__nombre_servicio": v["tipo_servicio__nombre_servicio"], "total": float(v["total"])} for v in ventas]
    return JsonResponse(ventas, safe=False)
