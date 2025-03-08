from django.contrib import admin
from .models import (
    Cliente, Vehiculo, CatalogoServicio, Servicio, DetalleServicio,
    Venta, Producto, ModuloBolsaAire, Cotizacion, DetalleCotizacion
)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'telefono', 'email', 'estado')
    search_fields = ('nombre', 'apellido', 'telefono', 'email')
    list_filter = ('estado',)

@admin.register(Vehiculo)
class VehiculoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'marca', 'modelo', 'anio', 'vin', 'tipo_motor')
    search_fields = ('marca', 'modelo', 'vin')
    list_filter = ('tipo_motor',)

@admin.register(CatalogoServicio)
class CatalogoServicioAdmin(admin.ModelAdmin):
    list_display = ('nombre_servicio', 'precio_base')
    search_fields = ('nombre_servicio',)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'vehiculo', 'fecha_servicio')
    search_fields = ('cliente__nombre', 'vehiculo__marca', 'vehiculo__modelo')
    date_hierarchy = 'fecha_servicio'

@admin.register(DetalleServicio)
class DetalleServicioAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'tipo_servicio', 'precio_final')

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_venta', 'monto_total')
    search_fields = ('cliente__nombre', 'cliente__apellido')
    date_hierarchy = 'fecha_venta'

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'cantidad', 'precio_unitario')  # Incluir precio_unitario
    search_fields = ('descripcion',)

@admin.register(ModuloBolsaAire)
class ModuloBolsaAireAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'fecha_reparacion', 'marca', 'modelo', 'numero_parte', 'tipo_microprocesador', 'precio_reparacion')
    search_fields = ('marca', 'modelo', 'numero_parte', 'tipo_microprocesador')
    date_hierarchy = 'fecha_reparacion'

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ('numero_cotizacion', 'fecha', 'cliente', 'vehiculo', 'total_general')
    search_fields = ('numero_cotizacion', 'cliente__nombre', 'vehiculo__marca')
    date_hierarchy = 'fecha'

@admin.register(DetalleCotizacion)
class DetalleCotizacionAdmin(admin.ModelAdmin):
    list_display = ('cotizacion', 'producto', 'cantidad', 'precio_unitario', 'precio_total')
