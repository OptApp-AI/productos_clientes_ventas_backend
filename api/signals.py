from django.dispatch import receiver
from django.db.models.signals import pre_delete, pre_save, post_save
import os
from django.core.files.storage import default_storage
from django.core.files import File

from .models import Producto, Empleado, Ruta, RutaDia
from django.contrib.auth.models import User


@receiver(pre_delete, sender=Producto)
def delete_producto_image(sender, instance, **kwargs):
    # Eliminar la imagen el producto si existe
    if instance.IMAGEN:
        if os.path.isfile(instance.IMAGEN.path):
            os.remove(instance.IMAGEN.path)


@receiver(pre_save, sender=Producto)
def delete_previous_producto_image(sender, instance, **kwargs):
    # Obtener el objeto Producto antes de la actualización
    if instance.pk:
        previous_producto = Producto.objects.get(pk=instance.pk)
        # Eliminar la imagen del producto si existe
        if previous_producto.IMAGEN and previous_producto.IMAGEN != instance.IMAGEN:
            if os.path.isfile(previous_producto.IMAGEN.path):
                os.remove(previous_producto.IMAGEN.path)


@receiver(pre_delete, sender=Empleado)
def delete_empleado_image(sender, instance, **kwargs):
    # Eliminar la imagen del empleado si existe
    if instance.IMAGEN:
        if os.path.isfile(instance.IMAGEN.path):
            os.remove(instance.IMAGEN.path)


@receiver(pre_save, sender=Empleado)
def delete_previous_producto_image(sender, instance, **kwargs):
    # Obtener el objeto Empleado antes de la actualización
    if instance.pk:
        previous_empleado = Empleado.objects.get(pk=instance.pk)
        # Eliminar la imagen del empleado si existe
        if previous_empleado.IMAGEN and previous_empleado.IMAGEN != instance.IMAGEN:
            if os.path.isfile(previous_empleado.IMAGEN.path):
                os.remove(previous_empleado.IMAGEN.path)


@receiver(pre_save, sender=Producto)
def set_default_product_image(sender, instance, **kwargs):
    # Asignar la imagen por default al producto si no se le asigno una
    if not instance.IMAGEN:
        default_image_path = "imagenes/default/producto_default.jpg"
        default_image = default_storage.open(default_image_path)
        instance.IMAGEN.save("producto_default.jpg", File(default_image), save=False)


@receiver(pre_save, sender=Empleado)
def set_default_employee_image(sender, instance, **kwargs):
    # Asignar la imagen por default al empleado si no se le asigno una
    if not instance.IMAGEN:
        default_image_path = "imagenes/default/usuario_default.png"
        default_image = default_storage.open(default_image_path)
        instance.IMAGEN.save("usuario_default.png", File(default_image), save=False)


@receiver(post_save, sender=User)
def create_empleado(sender, instance, created, **kwargs):
    if created:
        Empleado.objects.create(USUARIO=instance)


@receiver(post_save, sender=User)
def save_empleado(sender, instance, **kwargs):
    try:
        instance.empleado.save()
    except:
        Empleado.objects.create(USUARIO=instance)


# Create a signal for post_save of Ruta that will create RutaDia instances for each day of the week when a new Ruta instance is created.
@receiver(post_save, sender=Ruta)
def create_rutadia(sender, instance, created, **kwargs):
    # Create RutaDia for each day when a new Ruta is created
    if created:
        days = [
            "LUNES",
            "MARTES",
            "MIERCOLES",
            "JUEVES",
            "VIERNES",
            "SABADO",
            "DOMINGO",
        ]
        for day in days:
            RutaDia.objects.create(
                RUTA=instance,
                REPARTIDOR=instance.REPARTIDOR,
                REPARTIDOR_NOMBRE=instance.REPARTIDOR_NOMBRE,
                DIA=day,
            )
