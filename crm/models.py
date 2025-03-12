from django.db import models
import re
from django.core.validators import RegexValidator, MinValueValidator
from django.db.models import Sum
from datetime import datetime,date


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


# Modelo CatalogoServicio
class CatalogoServicio(models.Model):
    nombre_servicio = models.CharField(max_length=100, unique=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])

    def __str__(self):
        return self.nombre_servicio


# Modelo Servicio
from django.db import models
from django.core.validators import MinValueValidator

class Servicio(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, null=True, blank=True)
    fecha_servicio = models.DateField(auto_now_add=True)
    tipo_servicio = models.ForeignKey('CatalogoServicio', on_delete=models.CASCADE)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Servicio {self.id} - {self.cliente}"

    def calcular_total(self):
        self.precio_final = self.tipo_servicio.precio_base
        self.save()

# Modelo DetalleServicio

# Modelo Venta
class Venta(models.Model):
    fecha_venta = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha_venta}"

    def calcular_total(self):
        """Calcula el monto_total de la venta basado en los detalles."""
        total = sum(detalle.precio_total for detalle in self.detalles.all())
        self.monto_total = total
        self.save()


# Modelo DetalleVenta
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """Calcula el precio_total basado en la cantidad y el precio_unitario."""
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.venta.calcular_total()  # Actualiza el total de la venta

    def __str__(self):
        return f"{self.producto.descripcion} - {self.cantidad} x ${self.precio_unitario}"


# Modelo Producto
class Producto(models.Model):
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.descripcion} - ${self.precio_unitario}"



# Modelo Marca
class Marca(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre

# Modelo Modelo de Vehículo
class Modelo(models.Model):
    nombre = models.CharField(max_length=50)
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE, related_name="modelos")

    def __str__(self):
        return f"{self.marca.nombre} - {self.nombre}"

# Modelo de Reparación de Módulo de Bolsa de Aire
class ModuloBolsaAire(models.Model):
    cliente = models.ForeignKey("Cliente", on_delete=models.CASCADE)
    fecha_reparacion = models.DateField(default=date.today)  # Fecha actual por defecto
    marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE)
    anio = models.IntegerField(choices=[(i, i) for i in range(2010, 2031)])  # Años de 2010 a 2030
    numero_parte = models.CharField(max_length=50, unique=True)
    tipo_microprocesador = models.CharField(max_length=50)
    precio_reparacion = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.marca.nombre} {self.modelo.nombre} {self.anio} - {self.numero_parte}"



# Modelo Cotizacion
class Cotizacion(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_cotizacion = models.DateField(default=date.today)  # ✔️ Ahora es editable
    tipo_servicio = models.ForeignKey('CatalogoServicio', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    descripcion = models.TextField(blank=True, null=True)
    aprobada = models.BooleanField(default=False)  
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_general = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def calcular_total(self):
        """Calcula la suma de todos los subtotales de los productos cotizados."""
        self.total_general = self.detallecotizacion_set.aggregate(total=models.Sum('subtotal'))['total'] or 0.00
        self.save()

    def __str__(self):
        return f"Cotización {self.id} - {self.cliente}"


class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="detallecotizacion_set")
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Nuevo campo

    def save(self, *args, **kwargs):
        """Calcula el subtotal al guardar."""
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.cotizacion.calcular_total()  # Actualiza el total de la cotización

    def __str__(self):
        return f"{self.producto.descripcion} - {self.cantidad} x ${self.precio_unitario}"

# Detalle de Producto
from django.db import models
from django.core.validators import MinValueValidator

class DetalleProducto(models.Model):
    cotizacion = models.ForeignKey('Cotizacion', on_delete=models.CASCADE, related_name='productos')
    producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        """Calcula el subtotal basado en cantidad y precio unitario."""
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)
        self.cotizacion.calcular_total()  # Actualiza el total de la cotización

    def __str__(self):
        return f"{self.producto.descripcion} - {self.cantidad} x ${self.precio_unitario}"


class DetalleServicio(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='detalles_servicio', null=True, blank=True)  # Nueva relación con Cotización
    servicio = models.ForeignKey(CatalogoServicio, on_delete=models.CASCADE)
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE, related_name='detalles')
    tipo_servicio = models.ForeignKey(CatalogoServicio, on_delete=models.CASCADE)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        """Calcula el precio_final basado en el precio_base del CatalogoServicio."""
        if not self.precio_final:
            self.precio_final = self.tipo_servicio.precio_base
        super().save(*args, **kwargs)
        self.servicio.calcular_total()  # Actualiza el total del servicio

    def __str__(self):
        return f"{self.tipo_servicio.nombre_servicio} - ${self.precio_final}"

