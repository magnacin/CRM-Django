from django.shortcuts import render, redirect
from .forms import ClienteForm, VehiculoForm, ServicioForm, DetalleServicioForm
from .models import Cliente, Vehiculo, Servicio, DetalleServicio, CatalogoServicio
from django.forms import inlineformset_factory


def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()

    return render(request, 'crm/cliente_form.html', {'form': form})


def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'crm/listar_clientes.html', {'clientes': clientes})

# Vistas para Registrar Vehiculos
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

# Vistas para Registrar Servicios
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

#Catalogo de servicios

def listar_catalogo_servicios(request):
    servicios = CatalogoServicio.objects.all()
    return render(request, 'crm/listar_catalogo_servicios.html', {'servicios': servicios})

def registrar_servicio_catalogo(request):
    if request.method == 'POST':
        form = CatalogoServicioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_catalogo_servicios')
    else:
        form = CatalogoServicioForm()

    return render(request, 'crm/catalogo_servicio_form.html', {'form': form})

def editar_servicio_catalogo(request, pk):
    servicio = CatalogoServicio.objects.get(pk=pk)
    if request.method == 'POST':
        form = CatalogoServicioForm(request.POST, instance=servicio)
        if form.is_valid():
            form.save()
            return redirect('listar_catalogo_servicios')
    else:
        form = CatalogoServicioForm(instance=servicio)

    return render(request, 'crm/catalogo_servicio_form.html', {'form': form})

def eliminar_servicio_catalogo(request, pk):
    servicio = CatalogoServicio.objects.get(pk=pk)
    if request.method == 'POST':
        servicio.delete()
        return redirect('listar_catalogo_servicios')
    return render(request, 'crm/eliminar_servicio_confirm.html', {'servicio': servicio})

# Vista Cotizaciones:
from django.forms import inlineformset_factory
from .models import Cotizacion, DetalleCotizacion
from .forms import CotizacionForm, DetalleCotizacionForm

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
# Vista de Productos
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm

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
    return render(request, 'crm/eliminar_producto_confirm.html', {'producto': producto})
