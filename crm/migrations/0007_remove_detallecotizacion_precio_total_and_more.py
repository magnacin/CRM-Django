# Generated by Django 5.1.6 on 2025-03-11 18:29

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_alter_cotizacion_fecha_cotizacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detallecotizacion',
            name='precio_total',
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='cotizacion',
            name='total_general',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='detallecotizacion',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='cotizacion',
            name='fecha_cotizacion',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='detallecotizacion',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='detallecotizacion',
            name='cotizacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detallecotizacion_set', to='crm.cotizacion'),
        ),
        migrations.AlterField(
            model_name='detallecotizacion',
            name='precio_unitario',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
