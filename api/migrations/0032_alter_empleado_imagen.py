# Generated by Django 4.1.7 on 2023-06-07 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_alter_producto_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='IMAGEN',
            field=models.ImageField(blank=True, null=True, upload_to='imagenes/empleados'),
        ),
    ]
