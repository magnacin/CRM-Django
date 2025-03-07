from django import forms
from django.core.exceptions import ValidationError
from .models import (
    Cliente, Vehiculo, Servicio, DetalleServicio, 
    Cotizacion, DetalleCotizacion, Producto, CatalogoServicio
)

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'apellido', 'telefono', 'email', 'estado']

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre', '').upper()
        apellido = cleaned_data.get('apellido', '').upper()

        if Cliente.objects.filter(nombre=nombre, apellido=apellido).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un cliente con el mismo nombre y apellido.')

        cleaned_data['nombre'] = nombre
        cleaned_data['apellido'] = apellido

        return cleaned_data

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '')

        if telefono and not self.validar_formato_telefono(telefono):
            raise ValidationError('El formato de teléfono debe ser 123-456-7890.')

        return telefono

    @staticmethod
    def validar_formato_telefono(telefono):
        import re
        return re.match(r'^\d{3}-\d{3}-\d{4}$', telefono) is not None

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

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['descripcion', 'precio_unitario', 'cantidad']

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion').upper()

        if Producto.objects.filter(descripcion=descripcion).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un producto con esta descripción.')

        return descripcion

class CatalogoServicioForm(forms.ModelForm):
    class Meta:
        model = CatalogoServicio
        fields = ['nombre_servicio', 'precio_base']

    def clean_nombre_servicio(self):
        nombre = self.cleaned_data.get('nombre_servicio').upper()

        if CatalogoServicio.objects.filter(nombre_servicio=nombre).exclude(pk=self.instance.pk).exists():
            raise ValidationError('Ya existe un servicio con este nombre.')

        return nombre
