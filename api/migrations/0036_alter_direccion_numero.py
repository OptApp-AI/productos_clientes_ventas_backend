# Generated by Django 4.1.7 on 2023-09-01 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0035_alter_cliente_telefono'),
    ]

    operations = [
        migrations.AlterField(
            model_name='direccion',
            name='NUMERO',
            field=models.CharField(max_length=200),
        ),
    ]
