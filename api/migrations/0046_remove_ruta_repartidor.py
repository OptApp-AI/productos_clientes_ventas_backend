# Generated by Django 4.1.7 on 2023-09-19 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0045_alter_ruta_repartidor_salidaruta_productosalidaruta_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ruta',
            name='REPARTIDOR',
        ),
    ]
