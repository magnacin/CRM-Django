from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum, F
from .models import DetalleCotizacion, Cotizacion

def actualizar_total_cotizacion(cotizacion_id):
    total = DetalleCotizacion.objects.filter(cotizacion_id=cotizacion_id).aggregate(
        total=Sum(F('cantidad') * F('precio_unitario'))
    )['total'] or 0

    Cotizacion.objects.filter(id=cotizacion_id).update(total=total)

@receiver([post_save, post_delete], sender=DetalleCotizacion)
def actualizar_total_al_guardar_eliminar(sender, instance, **kwargs):
    actualizar_total_cotizacion(instance.cotizacion_id)
