# Generated by Django 4.1.7 on 2023-09-19 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0050_alter_cliente_rutas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='RUTAS',
            field=models.ManyToManyField(blank=True, to='api.ruta'),
        ),
    ]
