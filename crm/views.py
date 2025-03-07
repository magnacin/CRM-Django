from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from .models import (
    Cliente, Vehiculo, Servicio, DetalleServicio, 
    Cotizacion, DetalleCotizacion, Producto, CatalogoServicio
)
from .forms import (
    ClienteForm, VehiculoForm, ServicioForm, DetalleServicioForm,
    CotizacionForm, DetalleCotizacionForm, ProductoForm, CatalogoServicioForm
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
    return render(request, 'crm/confirmar_eliminar.html', {'obj': cliente})


# --- VEHICULOS ---
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
    return render(request, 'crm/confirmar_eliminar.html', {'obj': vehiculo})


# --- SERVICIOS ---
def listar_servicios(request):
    servicios = Servicio.objects.select_related('cliente', 'vehiculo').all()
    return render(request, 'crm/listar_servicios.html', {'servicios': servicios})

def registrar_servicio(request):
    DetalleServicioFormSet = inlineformset_factory(
        Servicio,
        DetalleServicio,
        form=DetalleServicioForm,
        extra=1,
        can_delete=False
    )

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


# --- COTIZACIONES ---
def listar_cotizaciones(request):
    cotizaciones = Cotizacion.objects.select_related('cliente', 'vehiculo').all()
    return render(request, 'crm/listar_cotizaciones.html', {'cotizaciones': cotizaciones})

def registrar_cotizacion(request):
    DetalleCotizacionFormSet = inlineformset_factory(
        Cotizacion,
        DetalleCotizacion,
        form=DetalleCotizacionForm,
        extra=1,
        can_delete=False
    )

    if request.method == 'POST':
        form = CotizacionForm(request.POST)
        formset = DetalleCotizacionFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            cotizacion = form.save()
            detalles = formset.save(commit=False)
            for detalle in detalles:
                detalle.cotizacion = cotizacion
                detalle.precio_total = detalle.cantidad * detalle.precio_unitario
                detalle.save()

            cotizacion.total_general = sum(d.precio_total for d in cotizacion.detallecotizacion_set.all())
            cotizacion.save()

            return redirect('listar_cotizaciones')
    else:
        form = CotizacionForm()
        formset = DetalleCotizacionFormSet()

    return render(request, 'crm/cotizacion_form.html', {'form': form, 'formset': formset})


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
    if request.method == 'POST':
        servicio.delete()
        return redirect('listar_servicios_catalogo')
    return render(request, 'crm/confirmar_eliminar.html', {'obj': servicio})
