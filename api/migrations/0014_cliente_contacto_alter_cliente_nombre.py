# Generated by Django 4.1.7 on 2023-04-05 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_cliente_correo_alter_cliente_telefono'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='CONTACTO',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='NOMBRE',
            field=models.CharField(max_length=200),
        ),
    ]
