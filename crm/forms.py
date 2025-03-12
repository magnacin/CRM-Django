from django import forms
from django.core.exceptions import ValidationError
from datetime import date
import re
from .models import (
    Cliente, Vehiculo, Servicio, DetalleServicio,
    Cotizacion, DetalleCotizacion, Producto, CatalogoServicio, ModuloBolsaAire, DetalleProducto
)
from django.forms import inlineformset_factory


# Funciones auxiliares reutilizables
def convertir_a_mayusculas(valor):
    """Convierte un valor a mayúsculas."""
    return valor.upper() if valor else valor


def validar_campo_unico(modelo, campo, valor, instancia=None):
    """Valida que un campo sea único en un modelo."""
    if valor:
        filtro = {campo: valor}
        queryset = modelo.objects.filter(**filtro)
        if instancia:
            queryset = queryset.exclude(pk=instancia.pk)
        if queryset.exists():
            raise ValidationError(f'Ya existe un registro con este {campo}.')


def formatear_telefono(telefono):
    """Formatea un número de teléfono a XXX-XXX-XXXX."""
    telefono = re.sub(r'\D', '', telefono)
    if len(telefono) != 10:
        raise ValidationError('El número de teléfono debe contener exactamente 10 dígitos.')
    return f'{telefono[:3]}-{telefono[3:6]}-{telefono[6:]}'


# Formularios
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'email', 'estado']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        return formatear_telefono(telefono)

    def clean(self):
        cleaned_data = super().clean()
        for field in ['nombre', 'apellido', 'email']:
            if field in cleaned_data:
                cleaned_data[field] = convertir_a_mayusculas(cleaned_data[field])
        return cleaned_data


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'marca', 'modelo', 'anio', 'vin', 'tipo_motor']

    def clean(self):
        cleaned_data = super().clean()
        for field in ['marca', 'modelo', 'vin']:
            if field in cleaned_data:
                cleaned_data[field] = convertir_a_mayusculas(cleaned_data[field])

        vin = cleaned_data.get('vin')
        marca = cleaned_data.get('marca')
        modelo = cleaned_data.get('modelo')
        anio = cleaned_data.get('anio')

        if vin:
            validar_campo_unico(Vehiculo, 'vin', vin, self.instance)
        elif Vehiculo.objects.filter(marca=marca, modelo=modelo, anio=anio).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un vehículo con la misma marca, modelo y año.')

        return cleaned_data


class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['cliente', 'vehiculo', 'tipo_servicio', 'descripcion']


class DetalleServicioForm(forms.ModelForm):
    tipo_servicio = forms.ModelChoiceField(
        queryset=CatalogoServicio.objects.all(),
        empty_label="Seleccione un servicio...",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    precio_final = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

    class Meta:
        model = DetalleServicio
        fields = ['tipo_servicio', 'precio_final']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'tipo_servicio' in self.initial:
            catalogo_servicio = CatalogoServicio.objects.get(pk=self.initial['tipo_servicio'])
            self.fields['precio_final'].initial = catalogo_servicio.precio_base

    def clean(self):
        cleaned_data = super().clean()
        tipo_servicio = cleaned_data.get('tipo_servicio')
        if tipo_servicio:
            cleaned_data['precio_final'] = tipo_servicio.precio_base
        return cleaned_data


# Formsets
DetalleServicioFormSet = inlineformset_factory(
    Servicio, DetalleServicio, form=DetalleServicioForm, extra=1, can_delete=True
)


class CotizacionForm(forms.ModelForm):
    fecha_cotizacion = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=True
    )

    class Meta:
        model = Cotizacion
        fields = ['cliente', 'vehiculo', 'fecha_cotizacion', 'tipo_servicio', 'precio_final', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehiculo'].queryset = Vehiculo.objects.none()
        self.fields['vehiculo'].required = False
        self.fields['vehiculo'].empty_label = "Vehículo no disponible"


class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacion
        exclude = ['subtotal']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'subtotal' in self.fields:
            self.fields['subtotal'].widget.attrs['readonly'] = True


DetalleCotizacionFormSet = inlineformset_factory(
    Cotizacion, DetalleCotizacion, form=DetalleCotizacionForm, extra=1, can_delete=True
)


class CatalogoServicioForm(forms.ModelForm):
    class Meta:
        model = CatalogoServicio
        fields = ['nombre_servicio', 'precio_base']

    def clean_nombre_servicio(self):
        nombre = convertir_a_mayusculas(self.cleaned_data.get('nombre_servicio'))
        validar_campo_unico(CatalogoServicio, 'nombre_servicio', nombre, self.instance)
        return nombre


from django import forms
from .models import ModuloBolsaAire, Cliente, Marca, Modelo

class ModuloBolsaAireForm(forms.ModelForm):
    nueva_marca = forms.CharField(required=False, max_length=50, label="Nueva Marca")
    nuevo_modelo = forms.CharField(required=False, max_length=50, label="Nuevo Modelo")

    class Meta:
        model = ModuloBolsaAire
        fields = ['cliente', 'marca', 'modelo', 'anio', 'numero_parte', 'tipo_microprocesador', 'precio_reparacion']
    
    fecha_reparacion = forms.DateField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),  # 🔹 Solo lectura
        initial=date.today,  # 🔹 Se inicializa con la fecha actual
        input_formats=['%d-%m-%Y'],  # 🔹 Formato día-mes-año
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filtrar modelos según la marca seleccionada
        self.fields['modelo'].queryset = Modelo.objects.none()

        if 'marca' in self.data:
            try:
                marca_id = int(self.data.get('marca'))
                self.fields['modelo'].queryset = Modelo.objects.filter(marca_id=marca_id).order_by('nombre')
            except (ValueError, TypeError):
                pass



class DetalleProductoForm(forms.ModelForm):
    class Meta:
        model = DetalleProducto
        fields = ['producto', 'cantidad', 'precio_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'subtotal' in self.fields:
            self.fields['subtotal'].widget.attrs['readonly'] = True