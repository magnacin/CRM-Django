from django.urls import path
from . import views

urlpatterns = [
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/nuevo/', views.registrar_cliente, name='registrar_cliente'),
    path('vehiculos/', views.listar_vehiculos, name='listar_vehiculos'),
    path('vehiculos/nuevo/', views.registrar_vehiculo, name='registrar_vehiculo'),
    path('servicios/', views.listar_servicios, name='listar_servicios'),
    path('servicios/nuevo/', views.registrar_servicio, name='registrar_servicio'),
    path('catalogo-servicios/', views.listar_catalogo_servicios, name='listar_catalogo_servicios'),
    path('catalogo-servicios/nuevo/', views.registrar_servicio_catalogo, name='registrar_servicio_catalogo'),
    path('catalogo-servicios/editar/<int:pk>/', views.editar_servicio_catalogo, name='editar_servicio_catalogo'),
    path('catalogo-servicios/eliminar/<int:pk>/', views.eliminar_servicio_catalogo, name='eliminar_servicio_catalogo'),
    path('cotizaciones/', views.listar_cotizaciones, name='listar_cotizaciones'),
    path('cotizaciones/nuevo/', views.registrar_cotizacion, name='registrar_cotizacion'),




]
