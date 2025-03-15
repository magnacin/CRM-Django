from django import forms
from django.core.exceptions import ValidationError
import re
from django import forms
from .models import Cliente, Vehiculo, Servicio, CatalogoServicio, ModuloReparacion, Venta

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


# 🔹 Formulario para Cliente
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


# 🔹 Formulario para Vehiculo
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


# 🔹 Formulario para Catálogo de Servicios
class CatalogoServicioForm(forms.ModelForm):
    class Meta:
        model = CatalogoServicio
        fields = ['nombre_servicio', 'precio_base']

    def clean_nombre_servicio(self):
        nombre = self.cleaned_data.get('nombre_servicio')
        return convertir_a_mayusculas(nombre)


# 🔹 Formulario para capturar un servicio
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['cliente', 'vehiculo', 'tipo_servicio', 'precio_final']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'vehiculo': forms.Select(attrs={'class': 'form-control'}),
            'tipo_servicio': forms.Select(attrs={'class': 'form-control'}),
            'precio_final': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(ServicioForm, self).__init__(*args, **kwargs)
        self.fields['tipo_servicio'].queryset = CatalogoServicio.objects.all()
        self.fields['precio_final'].widget.attrs['readonly'] = True  # Se llenará automáticamente con el precio base


# 🔹 Formulario para capturar datos de reparación de módulo
class ModuloReparacionForm(forms.ModelForm):
    class Meta:
        model = ModuloReparacion
        fields = ['marca', 'modelo', 'numero_parte', 'tipo_microprocesador', 'precio_reparacion']
        widgets = {
            'marca': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_parte': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_microprocesador': forms.TextInput(attrs={'class': 'form-control'}),
            'precio_reparacion': forms.NumberInput(attrs={'class': 'form-control'}),
        }

# Formulario para Servicios
class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['cliente', 'vehiculo', 'tipo_servicio', 'fecha_servicio', 'precio_final']

# Formulario para Catálogo de Servicios
class CatalogoServicioForm(forms.ModelForm):
    class Meta:
        model = CatalogoServicio
        fields = ['nombre_servicio', 'precio_base']

# Formulario para Reparación de Módulo
class ModuloReparacionForm(forms.ModelForm):
    class Meta:
        model = ModuloReparacion
        fields = ['cliente', 'marca', 'modelo', 'numero_parte', 'tipo_microprocesador', 'fecha_reparacion', 'precio_reparacion']
