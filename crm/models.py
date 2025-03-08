from django.db import models
import re
from django.core.validators import RegexValidator, MinValueValidator
from django.db.models import Sum
# from .models import Cliente, Vehiculo, Producto

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

class Vehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True, null=True, blank=True)
    tipo_motor = models.CharField(max_length=20, choices=[('Gasolina', 'Gasolina'), ('Diesel', 'Diesel'), ('Híbrido', 'Híbrido')])

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.anio}"

class CatalogoServicio(models.Model):
    nombre_servicio = models.CharField(max_length=100, unique=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre_servicio

class Servicio(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, null=True, blank=True)
    fecha_servicio = models.DateField(auto_now_add=True)

class DetalleServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    tipo_servicio = models.ForeignKey(CatalogoServicio, on_delete=models.CASCADE)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)



# Modelo Venta
class Venta(models.Model):
    fecha_venta = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha_venta}"

# Modelo Producto (detalle de venta)
class Producto(models.Model):
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    #def save(self, *args, **kwargs):
    #    self.descripcion = self.descripcion.upper()
    #    super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.descripcion} - ${self.precio_unitario}"

# Modelo ModuloBolsaAire
class ModuloBolsaAire(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_reparacion = models.DateField()
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    numero_parte = models.CharField(max_length=50, unique=True)
    tipo_microprocesador = models.CharField(max_length=50)
    precio_reparacion = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.marca} {self.modelo} {self.anio} - {self.numero_parte}"


# Modelo Cotizacion
from django.db import models
from datetime import datetime

class Cotizacion(models.Model):
    fecha = models.DateField(default=datetime.today)  # Se mantiene con fecha actual
    numero_cotizacion = models.PositiveIntegerField(unique=True)  # ❌ Quitar auto_created=True
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.SET_NULL, null=True, blank=True)
    total_general = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        """Autogenerar el número de cotización solo si es nuevo"""
        if not self.pk:  # Solo si es un nuevo registro
            max_num = Cotizacion.objects.aggregate(models.Max('numero_cotizacion'))['numero_cotizacion__max']
            self.numero_cotizacion = (max_num + 1) if max_num else 1  # ✅ Generación manual
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cotización {self.numero_cotizacion} - {self.cliente}"

    def calcular_total(self):
        total = sum(detalle.precio_total for detalle in self.detallecotizacion_set.all())
        self.total_general = total
        self.save()


class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.cotizacion.calcular_total()