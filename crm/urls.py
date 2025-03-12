from django.urls import path
from . import views
from .views import (
    listar_clientes, registrar_cliente, editar_cliente, eliminar_cliente,
    listar_vehiculos, registrar_vehiculo, editar_vehiculo, eliminar_vehiculo,
    listar_servicios, registrar_servicio, editar_servicio, eliminar_servicio,
    listar_servicios_catalogo, registrar_servicio_catalogo, editar_servicio_catalogo, eliminar_servicio_catalogo,
    listar_productos, registrar_producto, editar_producto, eliminar_producto, listar_cotizaciones, registrar_cotizacion, eliminar_cotizacion,
    obtener_precio_producto, editar_cotizacion, obtener_vehiculos_por_cliente, ajax_vehiculos, registrar_reparacion, listar_reparaciones
)

urlpatterns = [
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/nuevo/', views.registrar_cliente, name='registrar_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    # Vehiculos
    path('vehiculos/', views.listar_vehiculos, name='listar_vehiculos'),
    path('vehiculos/nuevo/', views.registrar_vehiculo, name='registrar_vehiculo'),
    path('vehiculos/editar/<int:pk>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:pk>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    path('ajax/vehiculos/cliente/<int:cliente_id>/', views.obtener_vehiculos_por_cliente, name='obtener_vehiculos_por_cliente'),
    path('ajax/vehiculos/<int:cliente_id>/', views.obtener_vehiculos_por_cliente, name='obtener_vehiculos_por_cliente'),
    # Servicios
    path('servicios/', views.listar_servicios, name='listar_servicios'),
    path('servicios/nuevo/', views.registrar_servicio, name='registrar_servicio'),
    path('servicios/editar/<int:pk>/', editar_servicio, name='editar_servicio'),
    path('servicios/eliminar/<int:pk>/', eliminar_servicio, name='eliminar_servicio'),
    path('servicios/modulo/<int:servicio_id>/', views.registrar_modulo_desde_servicio, name='registrar_modulo_desde_servicio'),
    # Catálogo de Servicios
    path('catalogo-servicios/', views.listar_servicios_catalogo, name='listar_servicios_catalogo'),
    path('catalogo-servicios/nuevo/', views.registrar_servicio_catalogo, name='registrar_servicio_catalogo'),
    path('catalogo-servicios/editar/<int:pk>/', views.editar_servicio_catalogo, name='editar_servicio_catalogo'),
    path('catalogo-servicios/eliminar/<int:pk>/', views.eliminar_servicio_catalogo, name='eliminar_servicio_catalogo'),
    # Cotizaciones
    path('cotizaciones/', listar_cotizaciones, name='listar_cotizaciones'),
    path('cotizaciones/nuevo/', registrar_cotizacion, name='registrar_cotizacion'),
    path('ajax/vehiculos/<int:cliente_id>/', ajax_vehiculos, name='ajax_vehiculos'),
    path('cotizaciones/eliminar/<int:pk>/', eliminar_cotizacion, name='eliminar_cotizacion'),
    path('cotizaciones/editar/<int:pk>/', editar_cotizacion, name='editar_cotizacion'),
    # Productos
    path('productos/', views.listar_productos, name='listar_productos'),
    path('productos/nuevo/', views.registrar_producto, name='registrar_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    path('productos/<int:producto_id>/precio/', obtener_precio_producto, name='obtener_precio_producto'),
    path("ajax/productos/", views.obtener_productos, name="ajax_productos"),
    path("ajax/servicios/", views.obtener_servicios, name="ajax_servicios"),
    path('modulos/nuevo/', registrar_reparacion, name='registrar_reparacion'),
    path('modulos/', listar_reparaciones, name='listar_reparaciones'),
]


