from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import (
    Cliente, Vehiculo, Servicio, DetalleServicio,
    Cotizacion, DetalleCotizacion, Producto, CatalogoServicio, ModuloBolsaAire
)
from .forms import (
    ClienteForm, VehiculoForm, ServicioForm, DetalleServicioForm,
    CotizacionForm, DetalleCotizacionForm, ProductoForm, CatalogoServicioForm, ModuloBolsaAireForm
)

# --- CLIENTES ---
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



# --- VEHICULOS ---from django.shortcuts import render, redirect, get_object_or_404
from .models import Vehiculo
from .forms import VehiculoForm

def listar_vehiculos(request):
    vehiculos = Vehiculo.objects.select_related('cliente').all()
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
    return render(request, 'crm/vehiculo_form.html', {'form': form})

def eliminar_vehiculo(request, pk):
    vehiculo = get_object_or_404(Vehiculo, pk=pk)
    if request.method == 'POST':
        vehiculo.delete()
        return redirect('listar_vehiculos')
    return render(request, 'crm/confirmar_eliminar.html', {'objeto': vehiculo})


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


# --- COTIZACIONES ---
def listar_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all()
    return render(request, 'crm/listar_cotizaciones.html', {'cotizaciones': cotizaciones})

def registrar_cotizacion(request):
    DetalleCotizacionFormSet = inlineformset_factory(Cotizacion, DetalleCotizacion, form=DetalleCotizacionForm, extra=3, can_delete=True)
    
    if request.method == "POST":
        form = CotizacionForm(request.POST)
        formset = DetalleCotizacionFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            cotizacion = form.save()
            detalles = formset.save(commit=False)
            total_general = 0
            for detalle in detalles:
                detalle.cotizacion = cotizacion
                detalle.precio_total = detalle.cantidad * detalle.precio_unitario
                total_general += detalle.precio_total
                detalle.save()
            cotizacion.total_general = total_general
            cotizacion.save()
            return redirect('listar_cotizaciones')
    else:
        form = CotizacionForm()
        formset = DetalleCotizacionFormSet()
    
    return render(request, 'crm/cotizacion_form.html', {'form': form, 'formset': formset})

def editar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    DetalleCotizacionFormSet = inlineformset_factory(Cotizacion, DetalleCotizacion, form=DetalleCotizacionForm, extra=1, can_delete=True)
    
    if request.method == "POST":
        form = CotizacionForm(request.POST, instance=cotizacion)
        formset = DetalleCotizacionFormSet(request.POST, instance=cotizacion)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            detalles = formset.save(commit=False)
            total_general = 0
            for detalle in detalles:
                detalle.precio_total = detalle.cantidad * detalle.precio_unitario
                total_general += detalle.precio_total
                detalle.save()
            cotizacion.total_general = total_general
            cotizacion.save()
            return redirect('listar_cotizaciones')
    else:
        form = CotizacionForm(instance=cotizacion)
        formset = DetalleCotizacionFormSet(instance=cotizacion)
    
    return render(request, 'crm/cotizacion_form.html', {'form': form, 'formset': formset})


def eliminar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.method == "POST":
        cotizacion.delete()
        return redirect('listar_cotizaciones')
    return render(request, 'crm/confirmar_eliminar.html', {'obj': cotizacion})



# --- PRODUCTOS ---
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

# --- SERVICIOS ---
def listar_servicios(request):
    servicios = Servicio.objects.all()

    for servicio in servicios:
        servicio.total_precio = sum(detalle.precio_final for detalle in servicio.detalleservicio_set.all())

    return render(request, 'crm/listar_servicios.html', {'servicios': servicios})


def registrar_servicio(request):
    DetalleServicioFormSet = inlineformset_factory(Servicio, DetalleServicio, form=DetalleServicioForm, extra=1)

    if request.method == 'POST':
        form = ServicioForm(request.POST)
        formset = DetalleServicioFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            servicio = form.save()
            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.servicio = servicio
                detalle.save()
            return redirect('listar_servicios')
    else:
        form = ServicioForm()
        formset = DetalleServicioFormSet()

    return render(request, 'crm/servicio_form.html', {'form': form, 'formset': formset})

def editar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    DetalleServicioFormSet = inlineformset_factory(Servicio, DetalleServicio, form=DetalleServicioForm, extra=0)

    if request.method == 'POST':
        form = ServicioForm(request.POST, instance=servicio)
        formset = DetalleServicioFormSet(request.POST, instance=servicio)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('listar_servicios')
    else:
        form = ServicioForm(instance=servicio)
        formset = DetalleServicioFormSet(instance=servicio)

    return render(request, 'crm/servicio_form.html', {'form': form, 'formset': formset})


def eliminar_servicio(request, pk):
    servicio = get_object_or_404(Servicio, pk=pk)
    if request.method == 'POST':
        servicio.delete()
        return redirect('listar_servicios')
    return render(request, 'crm/confirmar_eliminar.html', {'objeto': servicio})



# --- CATALOGO DE SERVICIOS ---
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
    servicio.delete()
    return redirect('listar_servicios_catalogo')


from django.http import JsonResponse
from .models import Producto

def obtener_precio_producto(request, producto_id):
    try:
        producto = Producto.objects.get(id=producto_id)
        return JsonResponse({'precio': producto.precio_unitario})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)