from django import forms
from django.db import models
import re   
from django.core.exceptions import ValidationError
from datetime import date, datetime
from .models import (
    Cliente, Vehiculo, Servicio, DetalleServicio, 
    Cotizacion, DetalleCotizacion, Producto, CatalogoServicio, ModuloBolsaAire
)

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'email', 'estado']

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        # Eliminar cualquier carácter que no sea dígito
        telefono = re.sub(r'\D', '', telefono)

        if len(telefono) != 10:
            raise ValidationError('El número de teléfono debe contener exactamente 10 dígitos.')

        # Formatear a XXX-XXX-XXXX
        telefono_formateado = f'{telefono[:3]}-{telefono[3:6]}-{telefono[6:]}'

        return telefono_formateado

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['nombre'] = cleaned_data.get('nombre', '').upper()
        cleaned_data['apellido'] = cleaned_data.get('apellido', '').upper()
        cleaned_data['email'] = cleaned_data.get('email', '').upper()
        return cleaned_data

class VehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehiculo
        fields = ['cliente', 'marca', 'modelo', 'anio', 'vin', 'tipo_motor']

    def clean(self):
        cleaned_data = super().clean()
        marca = cleaned_data.get('marca', '').upper()
        modelo = cleaned_data.get('modelo', '').upper()
        anio = cleaned_data.get('anio')
        vin = cleaned_data.get('vin', '').upper()

        if vin:
            if Vehiculo.objects.filter(vin=vin).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Ya existe un vehículo con ese VIN.')
        else:
            if Vehiculo.objects.filter(marca=marca, modelo=modelo, anio=anio).exclude(pk=self.instance.pk).exists():
                raise ValidationError('Ya existe un vehículo con la misma marca, modelo y año.')

        cleaned_data['marca'] = marca
        cleaned_data['modelo'] = modelo
        cleaned_data['vin'] = vin

        return cleaned_data
from datetime import date

from django import forms
from .models import Cliente, Vehiculo, Servicio, DetalleServicio, CatalogoServicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['cliente', 'vehiculo']  # Ya no incluimos fecha_servicio

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehiculo'].required = False  # Vehículo opcional



class DetalleServicioForm(forms.ModelForm):
    tipo_servicio = forms.ModelChoiceField(
        queryset=CatalogoServicio.objects.all(),
        empty_label="-- Selecciona un servicio --"
    )

    class Meta:
        model = DetalleServicio
        fields = ['tipo_servicio', 'precio_final']
from django import forms
from .models import Cotizacion

class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = ['fecha', 'numero_cotizacion', 'cliente', 'vehiculo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ✅ Asignar automáticamente la fecha actual si no se proporciona
        if not self.instance.pk:
            self.fields['fecha'].initial = datetime.today().strftime('%Y-%m-%d')

        # ✅ Generar el próximo número de cotización
        if not self.instance.pk:
            max_num = Cotizacion.objects.all().aggregate(models.Max('numero_cotizacion'))['numero_cotizacion__max']
            self.fields['numero_cotizacion'].initial = (max_num + 1) if max_num else 1


class DetalleCotizacionForm(forms.ModelForm):
    class Meta:
        model = DetalleCotizacion
        fields = ['producto', 'cantidad', 'precio_unitario']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields['precio_unitario'].widget.attrs.update({'readonly': 'false'})  # Sigue bloqueado, pero ahora lo rellenaremos automáticamente

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['descripcion', 'precio_unitario', 'cantidad']

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion').upper()

        if Producto.objects.filter(descripcion=descripcion).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un producto con esta descripción.')

        return descripcion
    def clean_precio_unitario(self):
        precio = self.cleaned_data.get('precio_unitario')
        if precio is None or precio <= 0:
            raise forms.ValidationError("El precio debe ser mayor a 0.")
        return precio

class CatalogoServicioForm(forms.ModelForm):
    class Meta:
        model = CatalogoServicio
        fields = ['nombre_servicio', 'precio_base']

    def clean_nombre_servicio(self):
        nombre = self.cleaned_data.get('nombre_servicio').upper()

        if CatalogoServicio.objects.filter(nombre_servicio=nombre).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un servicio con este nombre.')

        return nombre
    
# Modulos de bolsas de aire:
class ModuloBolsaAireForm(forms.ModelForm):
    class Meta:
        model = ModuloBolsaAire
        fields = ['marca', 'modelo', 'anio', 'numero_parte', 'tipo_microprocesador', 'precio_reparacion']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk and 'initial' not in kwargs:
            self.initial['fecha_reparacion'] = date.today().strftime('%d-%m-%Y')

    def clean_numero_parte(self):
        numero_parte = self.cleaned_data.get('numero_parte').upper()
        if ModuloBolsaAire.objects.filter(numero_parte=numero_parte).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un módulo con este número de parte.')
        return numero_parte

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data['marca'] = cleaned_data.get('marca', '').upper()
        cleaned_data['modelo'] = cleaned_data.get('modelo', '').upper()
        cleaned_data['numero_parte'] = cleaned_data.get('numero_parte', '').upper()
        return cleaned_data