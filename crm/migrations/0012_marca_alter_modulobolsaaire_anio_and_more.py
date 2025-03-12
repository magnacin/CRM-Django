# Generated by Django 4.2.5 on 2025-03-12 22:30

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0011_alter_servicio_tipo_servicio'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='modulobolsaaire',
            name='anio',
            field=models.IntegerField(choices=[(2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023), (2024, 2024), (2025, 2025), (2026, 2026), (2027, 2027), (2028, 2028), (2029, 2029), (2030, 2030)]),
        ),
        migrations.AlterField(
            model_name='modulobolsaaire',
            name='fecha_reparacion',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.CreateModel(
            name='Modelo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='modelos', to='crm.marca')),
            ],
        ),
        migrations.AlterField(
            model_name='modulobolsaaire',
            name='marca',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.marca'),
        ),
        migrations.AlterField(
            model_name='modulobolsaaire',
            name='modelo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.modelo'),
        ),
    ]
