from django.urls import path
from . import views

urlpatterns = [
    # Menu principal
    path('menu/', views.menu_principal, name='menu_principal'),

    # 🔹 Clientes
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/nuevo/', views.registrar_cliente, name='registrar_cliente'),
    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),

    # 🔹 Vehículos
    path('vehiculos/', views.listar_vehiculos, name='listar_vehiculos'),
    path('vehiculos/nuevo/', views.registrar_vehiculo, name='registrar_vehiculo'),
    path('vehiculos/editar/<int:pk>/', views.editar_vehiculo, name='editar_vehiculo'),
    path('vehiculos/eliminar/<int:pk>/', views.eliminar_vehiculo, name='eliminar_vehiculo'),
    path('ajax/vehiculos/cliente/<int:cliente_id>/', views.obtener_vehiculos_por_cliente, name='obtener_vehiculos_por_cliente'),

    # Catálogo de Servicios
    path('catalogo_servicios/', views.listar_catalogo_servicios, name='listar_catalogo_servicios'),
    path('catalogo_servicios/nuevo/', views.registrar_catalogo_servicio, name='registrar_catalogo_servicio'),

    # Servicios
    path('servicios/', views.listar_servicios, name='listar_servicios'),
    path('servicios/nuevo/', views.registrar_servicio, name='registrar_servicio'),

    # Reparaciones de Módulos
    path('reparaciones/', views.listar_reparaciones, name='listar_reparaciones'),
    path('reparaciones/nuevo/', views.registrar_reparacion, name='registrar_reparacion'),
    # Ventas
    path('ventas/', views.listar_ventas, name='listar_ventas'),
    path('reportes/ventas/', views.reporte_ventas, name='reporte_ventas'),


]
