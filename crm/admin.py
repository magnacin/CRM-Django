from django.contrib import admin
from .models import Cliente, Vehiculo

# Registrar Cliente y Vehiculo en el panel de administración
admin.site.register(Cliente)
admin.site.register(Vehiculo)
