from django import forms
from .models import Cliente, Vehiculo, Servicio, DetalleServicio, CatalogoServicio

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'email', 'estado']

    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        import re
        if not re.match(r'^\d{3}-\d{3}-\d{4}$', telefono):
            raise forms.ValidationError("El teléfono debe tener el formato 123-456-7890")
        return telefono
# Añadimos la forma para capturar vehiculos:
class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'marca', 'modelo', 'anio', 'vin', 'tipo_motor']

# Servicios
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['cliente', 'vehiculo', 'fecha_servicio']

class DetalleServicioForm(forms.ModelForm):
    tipo_servicio = forms.ModelChoiceField(
        queryset=CatalogoServicio.objects.all(),
        empty_label="-- Selecciona un servicio --"
    )

    class Meta:
        model = DetalleServicio
        fields = ['tipo_servicio', 'precio_final']

from .models import CatalogoServicio

class CatalogoServicioForm(forms.ModelForm):
    class Meta:
        model = CatalogoServicio
        fields = ['nombre_servicio', 'precio_base']

# Cotizaciones:
from .models import Cotizacion, DetalleCotizacion, Producto

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['cliente', 'vehiculo', 'fecha']

class DetalleCotizacionForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        empty_label="-- Selecciona un producto --"
    )

    class Meta:
        model = DetalleCotizacion
        fields = ['producto', 'cantidad', 'precio_unitario', 'precio_total']

