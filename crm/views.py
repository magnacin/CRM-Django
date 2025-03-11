from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from django.db.models import Q
from datetime import date, datetime
from django.http import JsonResponse  # Nueva importación
from .models import (
    Cliente, Vehiculo, Servicio, DetalleServicio, 
    Cotizacion, DetalleCotizacion, Producto, CatalogoServicio, ModuloBolsaAire
)
from .forms import (
    ClienteForm, VehiculoForm, ServicioForm, DetalleServicioForm,
    CotizacionForm, DetalleCotizacionForm,CatalogoServicioForm, ModuloBolsaAireForm # ProductoForm, 
)

# Funciones auxiliares reutilizables
def convertir_a_mayusculas(valor):
    """Convierte un valor a mayúsculas."""
    return valor.upper() if valor else valor


def validar_campo_unico(modelo, campo, valor, instancia=None):
    """Valida que un campo sea único en un modelo."""
    if valor:
        filtro = {campo: valor}
        queryset = modelo.objects.filter(**filtro)
        if instancia:
            queryset = queryset.exclude(pk=instancia.pk)
        if queryset.exists():
            raise ValidationError(f'Ya existe un registro con este {campo}.')


# Vistas para Clientes
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


# Vistas para Vehículos
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


# Vistas para Servicios
from django.shortcuts import render
from .models import Servicio

def listar_servicios(request):
    servicios = Servicio.objects.all().select_related('cliente', 'vehiculo').prefetch_related('detalles')
    return render(request, 'crm/listar_servicios.html', {'servicios': servicios})


def registrar_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_servicios')
    else:
        form = ServicioForm()
    return render(request, 'crm/servicio_form.html', {'form': form})


def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('listar_servicios')
    else:
        form = ServicioForm(instance=servicio)
    return render(request, 'crm/servicio_form.html', {'form': form})


def eliminar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        return redirect('listar_servicios')
    return render(request, 'crm/confirmar_eliminar.html', {'objeto': servicio})


# Vistas para Catálogo de Servicios
from django.shortcuts import render
from .models import CatalogoServicio

def listar_servicios_catalogo(request):
    servicios = CatalogoServicio.objects.all()
    return render(request, 'crm/listar_servicios_catalogo.html', {'servicios': servicios})


def registrar_servicio_catalogo(request):
    if request.method == 'POST':
        form = CatalogoServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_servicios_catalogo')
    else:
        form = CatalogoServicioForm()
    return render(request, 'crm/servicio_catalogo_form.html', {'form': form})


def editar_servicio_catalogo(request, pk):
    servicio = get_object_or_404(CatalogoServicio, pk=pk)
    if request.method == 'POST':
        form = CatalogoServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('listar_servicios_catalogo')
    else:
        form = CatalogoServicioForm(instance=servicio)
    return render(request, 'crm/servicio_catalogo_form.html', {'form': form})


def eliminar_servicio_catalogo(request, pk):
    servicio = get_object_or_404(CatalogoServicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        return redirect('listar_servicios_catalogo')
    return render(request, 'crm/confirmar_eliminar.html', {'objeto': servicio})


# Vistas para Productos
def listar_productos(request):
    productos = Producto.objects.all()
    return render(request, 'crm/listar_productos.html', {'productos': productos})


def registrar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm()
    return render(request, 'crm/producto_form.html', {'form': form})


def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('listar_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'crm/producto_form.html', {'form': form})


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('listar_productos')
    return render(request, 'crm/confirmar_eliminar.html', {'obj': producto})


# Vistas para Cotizaciones
def listar_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all()
    return render(request, 'crm/listar_cotizaciones.html', {'cotizaciones': cotizaciones})

from django.shortcuts import render, redirect
from .models import Cotizacion, CatalogoServicio
from .forms import CotizacionForm

def crear_cotizacion(request):
    if request.method == 'POST':
        form = CotizacionForm(request.POST)
        if form.is_valid():
            cotizacion = form.save()
            cotizacion.calcular_total()  # Calcula el precio final
            return redirect('listar_cotizaciones')
    else:
        form = CotizacionForm()
    return render(request, 'crear_cotizacion.html', {'form': form})



from django.forms import inlineformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cotizacion, DetalleCotizacion, CatalogoServicio
from .forms import CotizacionForm, DetalleCotizacionForm, DetalleProductoForm, DetalleProducto

def registrar_cotizacion(request):
    DetalleProductoFormSet = inlineformset_factory(
        Cotizacion,
        DetalleProducto,
        form=DetalleProductoForm,
        extra=1,
        can_delete=True
    )
    DetalleServicioFormSet = inlineformset_factory(
        Cotizacion,
        DetalleServicio,
        form=DetalleServicioForm,
        extra=1,
        can_delete=True
    )

    if request.method == "POST":
        form = CotizacionForm(request.POST)
        formset_productos = DetalleProductoFormSet(request.POST, prefix="productos")
        formset_servicios = DetalleServicioFormSet(request.POST, prefix="servicios")

        if form.is_valid() and formset_productos.is_valid() and formset_servicios.is_valid():
            cotizacion = form.save()
            formset_productos.instance = cotizacion
            formset_productos.save()
            formset_servicios.instance = cotizacion
            formset_servicios.save()
            return redirect('listar_cotizaciones')
    else:
        form = CotizacionForm()
        formset_productos = DetalleProductoFormSet(prefix="productos")
        formset_servicios = DetalleServicioFormSet(prefix="servicios")

    return render(request, 'crm/cotizacion_form.html', {
        'form': form,
        'formset_productos': formset_productos,
        'formset_servicios': formset_servicios
    })


def editar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.method == 'POST':
        form = CotizacionForm(request.POST, instance=cotizacion)
        if form.is_valid():
            form.save()
            return redirect('listar_cotizaciones')
    else:
        form = CotizacionForm(instance=cotizacion)
    return render(request, 'crm/cotizacion_form.html', {'form': form})


def eliminar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.method == 'POST':
        cotizacion.delete()
        return redirect('listar_cotizaciones')
    return render(request, 'crm/confirmar_eliminar.html', {'obj': cotizacion})


# Función para registrar un módulo desde servicio
def registrar_modulo_desde_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)

    if request.method == 'POST':
        form = ModuloBolsaAireForm(request.POST)
        if form.is_valid():
            modulo = form.save(commit=False)
            modulo.cliente = servicio.cliente
            modulo.fecha_reparacion = servicio.fecha_servicio
            modulo.save()
            return redirect('listar_servicios')
    else:
        form = ModuloBolsaAireForm(initial={
            'cliente': servicio.cliente,
            'fecha_reparacion': servicio.fecha_servicio
        })

    return render(request, 'crm/modulo_form.html', {'form': form})


# Vista para obtener el precio de un producto
def obtener_precio_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return JsonResponse({'precio': producto.precio_unitario})


# Nueva vista para obtener vehículos por cliente
def obtener_vehiculos_por_cliente(request, cliente_id):
    vehiculos = Vehiculo.objects.filter(cliente_id=cliente_id).values('id', 'marca', 'modelo', 'anio')
    return JsonResponse(list(vehiculos), safe=False)

from django.shortcuts import render, redirect
from .models import Servicio, DetalleServicio, CatalogoServicio
from .forms import ServicioForm, DetalleServicioFormSet

from django.shortcuts import render, redirect
from .forms import ServicioForm, DetalleServicioFormSet

def crear_servicio(request):
    if request.method == 'POST':
        form = ServicioForm(request.POST)
        if form.is_valid():
            servicio = form.save()
            servicio.calcular_total()  # Calcula el precio final
            return redirect('listar_servicios')
    else:
        form = ServicioForm()
    return render(request, 'crear_servicio.html', {'form': form})


from django.http import JsonResponse
from .models import Vehiculo

def ajax_vehiculos(request, cliente_id):
    vehiculos = Vehiculo.objects.filter(cliente_id=cliente_id).values('id', 'marca', 'modelo', 'anio')
    return JsonResponse(list(vehiculos), safe=False)