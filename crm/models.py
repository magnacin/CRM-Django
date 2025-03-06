from django.db import models
import re

# Modelo Cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=12)
    email = models.EmailField()
    estado = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.nombre = self.nombre.upper()
        self.apellido = self.apellido.upper()
        self.email = self.email.upper()
        if not re.match(r'^\d{3}-\d{3}-\d{4}$', self.telefono):
            raise ValueError("El telefono debe estar en formato 123-456-7890")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

# Modelo Vehiculo
class Vehiculo(models.Model):
    TIPO_MOTOR_CHOICES = [
        ('GASOLINA', 'Gasolina'),
        ('DIESEL', 'Diésel'),
        ('HIBRIDO', 'Híbrido'),
        ('ELECTRICO', 'Eléctrico'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    anio = models.IntegerField()
    vin = models.CharField(max_length=17, unique=True)
    tipo_motor = models.CharField(max_length=10, choices=TIPO_MOTOR_CHOICES)

    def save(self, *args, **kwargs):
        self.marca = self.marca.upper()
        self.modelo = self.modelo.upper()
        self.vin = self.vin.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.anio})"

# Modelo CatalogoServicio
class CatalogoServicio(models.Model):
    nombre_servicio = models.CharField(max_length=100, unique=True)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.nombre_servicio = self.nombre_servicio.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_servicio

# Modelo Servicio
class Servicio(models.Model):
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_servicio = models.DateField()

    def __str__(self):
        return f"Servicio {self.id} - {self.fecha_servicio}"

# Modelo DetalleServicio
class DetalleServicio(models.Model):
    servicio = models.ForeignKey(Servicio, on_delete=models.CASCADE)
    tipo_servicio = models.ForeignKey(CatalogoServicio, on_delete=models.PROTECT)
    precio_final = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.tipo_servicio.nombre_servicio} - ${self.precio_final}"

# Modelo Venta
class Venta(models.Model):
    fecha_venta = models.DateField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Venta {self.id} - {self.fecha_venta}"

# Modelo Producto (detalle de venta)
class Producto(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.descripcion} - {self.cantidad} piezas"

# Modelo ModuloBolsaAire
class ModuloBolsaAire(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_reparacion = models.DateField()
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    numero_parte = models.CharField(max_length=50)
    tipo_microprocesador = models.CharField(max_length=50)
    precio_reparacion = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.marca = self.marca.upper()
        self.modelo = self.modelo.upper()
        self.numero_parte = self.numero_parte.upper()
        self.tipo_microprocesador = self.tipo_microprocesador.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.marca} {self.modelo} - {self.numero_parte}"

# Modelo Cotizacion
class Cotizacion(models.Model):
    fecha = models.DateField()
    numero_cotizacion = models.IntegerField(unique=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Cotizacion {self.numero_cotizacion}"

# Modelo DetalleCotizacion
class DetalleCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="detalles")
    descripcion = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=12, decimal_places=2)

    def save(self, *args, **kwargs):
        self.descripcion = self.descripcion.upper()
        self.precio_total = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return self.descripcion
