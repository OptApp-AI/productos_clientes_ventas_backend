# Generated by Django 4.1.7 on 2023-09-02 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_productoventa_nombre_producto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productoventa',
            name='NOMBRE_PRODUCTO',
            field=models.CharField(max_length=200),
        ),
    ]