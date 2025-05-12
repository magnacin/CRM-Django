from django.db import models
import re
from django.core.validators import RegexValidator, MinValueValidator
from django.db.models import Sum
from datetime import datetime, date

# Modelo Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(
        max_length=12,
        validators=[RegexValidator(r'^\d{3}-\d{3}-\d{4}$', message="Formato de teléfono inválido (XXX-XXX-XXXX).")]
    )
    email = models.EmailField()
    estado = models.CharField(max_length=20, choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')])

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo Vehiculo
class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True, null=True, blank=True)
    tipo_motor = models.CharField(max_length=20, choices=[('Gasolina', 'Gasolina'), ('Diesel', 'Diesel'), ('Híbrido', 'Híbrido')])

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.anio}"

# 🔹 Modelo Catálogo de Servicios
class CatalogoServicio(models.Model):
    nombre_servicio = models.CharField(max_length=100, unique=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return self.nombre_servicio

# 🔹 Modelo Servicio (Relaciona Cliente y Vehículo opcionalmente)
class Servicio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True, blank=True)  # Opcional
    fecha_servicio = models.DateField(default=date.today)
    tipo_servicio = models.ForeignKey(CatalogoServicio, on_delete=models.CASCADE)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return f"{self.tipo_servicio} - {self.cliente}"

    def save(self, *args, **kwargs):
        """Asigna el precio base si no se proporciona un precio final."""
        if not self.precio_final:
            self.precio_final = self.tipo_servicio.precio_base
        super().save(*args, **kwargs)

# 🔹 Modelo Reparación de Módulo (Opcional dentro de Servicio)
class ModuloReparacion(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con Cliente
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    numero_parte = models.CharField(max_length=50, unique=True)
    tipo_microprocesador = models.CharField(max_length=50)
    fecha_reparacion = models.DateField(default=date.today)  # ya esta definido en servicio
    precio_reparacion = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.numero_parte}"

# 🔹 Modelo Venta (Se crea automáticamente al registrar un servicio)
class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    fecha_venta = models.DateField(auto_now_add=True)  # Tomar la fecha de registro del servicio
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """ Al guardar una venta, tomar los datos desde Servicio """
        if self.servicio:
            self.fecha_venta = self.servicio.fecha_servicio  # Fecha de servicio
            self.monto_total = self.servicio.precio_final  # Precio del servicio
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Venta de {self.servicio.tipo_servicio} - {self.monto_total} el {self.fecha_venta}"

class Cotizacion(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    numero_cotizacion = models.PositiveIntegerField(unique=True)

    # Nuevos campos reemplazando 'vehiculo'
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()

    total_general = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calcular_total(self):
        total = sum(detalle.precio_total for detalle in self.detallecotizacion_set.all())
        self.total_general = total
        self.save()

    def __str__(self):
        return f"Cotización #{self.numero_cotizacion} - {self.cliente}"

class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey('Cotizacion', on_delete=models.CASCADE)
    tipo_servicio = models.ForeignKey('CatalogoServicio', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.cotizacion.calcular_total()

    def __str__(self):
        return f"{self.tipo_servicio} x {self.cantidad} (${self.precio_total})"
