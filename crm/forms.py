from django import forms
from django.db import models
import re
from django.core.exceptions import ValidationError
from datetime import date, datetime
from .models import (
    Cliente, Vehiculo, Servicio, DetalleServicio,
    Cotizacion, DetalleCotizacion, Producto, CatalogoServicio, ModuloBolsaAire
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
        cleaned_data['nombre'] = convertir_a_mayusculas(cleaned_data.get('nombre', ''))
        cleaned_data['apellido'] = convertir_a_mayusculas(cleaned_data.get('apellido', ''))
        cleaned_data['email'] = convertir_a_mayusculas(cleaned_data.get('email', ''))
        return cleaned_data


class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'marca', 'modelo', 'anio', 'vin', 'tipo_motor']

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['marca'] = convertir_a_mayusculas(cleaned_data.get('marca', ''))
        cleaned_data['modelo'] = convertir_a_mayusculas(cleaned_data.get('modelo', ''))
        cleaned_data['vin'] = convertir_a_mayusculas(cleaned_data.get('vin', ''))

        vin = cleaned_data.get('vin')
        marca = cleaned_data.get('marca')
        modelo = cleaned_data.get('modelo')
        anio = cleaned_data.get('anio')

        if vin:
            validar_campo_unico(Vehiculo, 'vin', vin, self.instance)
        else:
            if Vehiculo.objects.filter(marca=marca, modelo=modelo, anio=anio).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Ya existe un vehículo con la misma marca, modelo y año.')

        return cleaned_data


from django import forms
from .models import Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['cliente', 'vehiculo', 'tipo_servicio', 'descripcion']


class DetalleServicioForm(forms.ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ['tipo_servicio', 'precio_final']

    tipo_servicio = forms.ModelChoiceField(
        queryset=CatalogoServicio.objects.all(),
        empty_label="Seleccione un servicio...",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    precio_final = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )

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


# Formset para DetalleServicio
DetalleServicioFormSet = inlineformset_factory(
    Servicio, DetalleServicio, form=DetalleServicioForm, extra=1, can_delete=True
)


from django import forms
from .models import Cotizacion
from django import forms
from .models import Cotizacion, Vehiculo

from django import forms
from .models import Cotizacion, Vehiculo

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['cliente', 'vehiculo', 'tipo_servicio', 'descripcion', 'fecha_cotizacion', 'precio_final', 'aprobada']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar una opción "Vehículo no disponible" al campo vehiculo
        self.fields['vehiculo'].queryset = Vehiculo.objects.none()  # Inicialmente sin vehículos
        self.fields['vehiculo'].required = False
        self.fields['vehiculo'].empty_label = "Vehículo no disponible"

class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacion
        fields = ['producto', 'cantidad', 'precio_unitario']


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['descripcion', 'precio_unitario', 'cantidad']

    def clean_descripcion(self):
        descripcion = convertir_a_mayusculas(self.cleaned_data.get('descripcion'))
        validar_campo_unico(Producto, 'descripcion', descripcion, self.instance)
        return descripcion

    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        if precio is None or precio <= 0:
            raise ValidationError("El precio debe ser mayor a 0.")
        return precio


class CatalogoServicioForm(forms.ModelForm):
    class Meta:
        model = CatalogoServicio
        fields = ['nombre_servicio', 'precio_base']

    def clean_nombre_servicio(self):
        nombre = convertir_a_mayusculas(self.cleaned_data.get('nombre_servicio'))
        validar_campo_unico(CatalogoServicio, 'nombre_servicio', nombre, self.instance)
        return nombre


class ModuloBolsaAireForm(forms.ModelForm):
    class Meta:
        model = ModuloBolsaAire
        fields = ['marca', 'modelo', 'anio', 'numero_parte', 'tipo_microprocesador', 'precio_reparacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and 'initial' not in kwargs:
            self.initial['fecha_reparacion'] = date.today().strftime('%d-%m-%Y')

    def clean_numero_parte(self):
        numero_parte = convertir_a_mayusculas(self.cleaned_data.get('numero_parte'))
        validar_campo_unico(ModuloBolsaAire, 'numero_parte', numero_parte, self.instance)
        return numero_parte

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['marca'] = convertir_a_mayusculas(cleaned_data.get('marca', ''))
        cleaned_data['modelo'] = convertir_a_mayusculas(cleaned_data.get('modelo', ''))
        cleaned_data['numero_parte'] = convertir_a_mayusculas(cleaned_data.get('numero_parte', ''))
        return cleaned_data