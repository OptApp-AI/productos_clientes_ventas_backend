# Generated by Django 4.1.7 on 2023-05-15 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_alter_cliente_correo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='CONTACTO',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
