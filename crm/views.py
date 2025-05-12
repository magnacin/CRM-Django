from django.shortcuts import render, get_object_or_404, redirect
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.db.models import Q, Sum
from datetime import date, datetime
from .models import Cliente, Vehiculo, Servicio, CatalogoServicio, ModuloReparacion, Venta
from .forms import ClienteForm, VehiculoForm, ServicioForm, CatalogoServicioForm, ModuloReparacionForm
import json
from django.http import JsonResponse


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


def reporte_ventas(request):
    clientes = Cliente.objects.all()
    ventas_por_servicio = Servicio.objects.values('tipo_servicio__nombre_servicio') \
        .annotate(total=Sum('precio_final'))
    ventas_por_servicio = [
        {"tipo_servicio__nombre_servicio": item["tipo_servicio__nombre_servicio"], "total": float(item["total"])}
        for item in ventas_por_servicio
    ]
    return render(request, 'crm/reporte_ventas.html', {
        'clientes': clientes,
        'ventas_por_servicio_json': json.dumps(ventas_por_servicio)
    })

def reporte_ventas_datos(request):
    cliente_id = request.GET.get("cliente_id")
    fecha_inicio = request.GET.get("fecha_inicio")
    fecha_fin = request.GET.get("fecha_fin")

    servicios = Servicio.objects.all()

    # ✅ Filtrar por cliente si se proporcionó
    if cliente_id:
        servicios = servicios.filter(cliente_id=cliente_id)

    # ✅ Validar fechas y aplicar filtros
    try:
        if fecha_inicio:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
            servicios = servicios.filter(fecha_servicio__gte=fecha_inicio)
        if fecha_fin:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
            servicios = servicios.filter(fecha_servicio__lte=fecha_fin)
    except Exception as e:
        return JsonResponse({"error": f"Formato de fecha inválido: {str(e)}"}, status=400)

    # ✅ Agrupar y sumar totales
    resumen = servicios.values("tipo_servicio__nombre_servicio") \
        .annotate(total=Sum("precio_final"))

    # ✅ Convertir a JSON serializable
    datos = []
    for r in resumen:
        datos.append({
            "tipo_servicio__nombre_servicio": r["tipo_servicio__nombre_servicio"],
            "total": float(r["total"]) if r["total"] else 0
        })

    return JsonResponse(datos, safe=False)



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

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max
from .models import Cotizacion, DetalleCotizacion
from .forms import CotizacionForm,DetalleCotizacionFormSet
from datetime import date

def listar_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all().order_by('-fecha', '-numero_cotizacion')
    return render(request, 'crm/listar_cotizaciones.html', {'cotizaciones': cotizaciones})

def listar_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all().order_by('-fecha', '-numero_cotizacion')
    return render(request, 'crm/listar_cotizaciones.html', {'cotizaciones': cotizaciones})


def registrar_cotizacion(request):
    from django.db.models import Max
    ultimo = Cotizacion.objects.aggregate(Max('numero_cotizacion'))['numero_cotizacion__max'] or 0
    numero_nuevo = ultimo + 1

    marcas = Cotizacion.objects.values_list('marca', flat=True).distinct()
    modelos = Cotizacion.objects.values_list('modelo', flat=True).distinct()
    anios = Cotizacion.objects.values_list('anio', flat=True).distinct()
    servicios = CatalogoServicio.objects.all()  # ✅ para el select dinámico

    if request.method == 'POST':
        form = CotizacionForm(request.POST)
        formset = DetalleCotizacionFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            cotizacion = form.save(commit=False)
            cotizacion.numero_cotizacion = numero_nuevo
            cotizacion.marca = request.POST.get('marca')
            cotizacion.modelo = request.POST.get('modelo')
            cotizacion.anio = request.POST.get('anio')
            cotizacion.save()

            formset.instance = cotizacion
            formset.save()
            return redirect('listar_cotizaciones')
    else:
        form = CotizacionForm()
        formset = DetalleCotizacionFormSet()

    return render(request, 'crm/cotizacion_form.html', {
        'form': form,
        'formset': formset,
        'numero_cotizacion': numero_nuevo,
        'marcas': marcas,
        'modelos': modelos,
        'anios': anios,
        'servicios': servicios  # ✅ pasa al template
    })



def editar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)

    marcas = Cotizacion.objects.values_list('marca', flat=True).distinct()
    modelos = Cotizacion.objects.values_list('modelo', flat=True).distinct()
    anios = Cotizacion.objects.values_list('anio', flat=True).distinct()
    servicios = CatalogoServicio.objects.all()

    if request.method == 'POST':
        form = CotizacionForm(request.POST, instance=cotizacion)
        formset = DetalleCotizacionFormSet(request.POST, instance=cotizacion)

        if form.is_valid() and formset.is_valid():
            cotizacion = form.save(commit=False)
            cotizacion.marca = request.POST.get('marca')
            cotizacion.modelo = request.POST.get('modelo')
            cotizacion.anio = request.POST.get('anio')
            cotizacion.save()

            formset.instance = cotizacion
            formset.save()

            return redirect('listar_cotizaciones')
        else:
            # Opcional: mensajes de error para debug si algo falla
            print("FORM ERRORS:", form.errors)
            print("FORMSET ERRORS:", formset.errors)

    else:
        form = CotizacionForm(instance=cotizacion)
        formset = DetalleCotizacionFormSet(instance=cotizacion)

    return render(request, 'crm/cotizacion_form.html', {
        'form': form,
        'formset': formset,
        'numero_cotizacion': cotizacion.numero_cotizacion,
        'marcas': marcas,
        'modelos': modelos,
        'anios': anios,
        'servicios': servicios
    })




def eliminar_cotizacion(request, pk):
    cotizacion = get_object_or_404(Cotizacion, pk=pk)
    if request.method == 'POST':
        cotizacion.delete()
        return redirect('listar_cotizaciones')
    return render(request, 'crm/confirmar_eliminar.html', {'obj': cotizacion})