from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Empleado(models.Model):
    USUARIO = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True, related_name="empleado"
    )
    # El problema de este codigo es que para los empleados creados si subir una imagen, su imagen vive en default folder, y cuando se borranr se borra tambien la imagen de default
    # IMAGEN = models.ImageField(
    #     default='imagenes/default/usuario_default.png', upload_to='imagenes/empleados')

    IMAGEN = models.ImageField(upload_to="imagenes/empleados", null=True, blank=True)

    def __str__(self):
        return f"Empleado con usuario: {self.USUARIO.username}"


# Create your models here.
class Producto(models.Model):
    NOMBRE = models.CharField(max_length=100)

    CANTIDAD = models.FloatField(validators=[MinValueValidator(0)])

    PRECIO = models.FloatField(validators=[MinValueValidator(0)])

    # IMAGEN = models.ImageField(
    #     default='imagenes/default/producto_default.jpg', upload_to='imagenes/productos')

    IMAGEN = models.ImageField(upload_to="imagenes/productos", null=True, blank=True)

    # RECUERDA NO PONER NADA QUE SE PUEDE VOLVER NULL AQUI
    def __str__(self):
        return f"{self.NOMBRE}, {self.CANTIDAD}, {self.PRECIO}"

    def save(self, *args, **kwargs):
        self.NOMBRE = self.NOMBRE.upper()

        super().save(*args, **kwargs)


class Direccion(models.Model):
    CALLE = models.CharField(max_length=200)
    NUMERO = models.CharField(max_length=200)
    COLONIA = models.CharField(max_length=200, null=True, blank=True)
    CIUDAD = models.CharField(max_length=200)
    MUNICIPIO = models.CharField(max_length=200, null=True, blank=True)
    CP = models.IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)

    class Meta:
        verbose_name_plural = "Direcciones"

    def __str__(self):
        return f"{self.CALLE}, {self.NUMERO}, {self.COLONIA}"

    def save(self, *args, **kwargs):
        self.CALLE = self.CALLE.upper()
        self.COLONIA = self.COLONIA.upper()
        self.CIUDAD = self.CIUDAD.upper()
        self.MUNICIPIO = self.MUNICIPIO.upper()
        super().save(*args, **kwargs)


class Cliente(models.Model):
    TIPOS_DE_PAGO = (
        ("EFECTIVO", "EFECTIVO"),
        ("CREDITO", "CREDITO"),
    )

    NOMBRE = models.CharField(max_length=200)

    CONTACTO = models.CharField(max_length=200, null=True, blank=True)

    DIRECCION = models.OneToOneField(
        Direccion, on_delete=models.CASCADE, null=True, blank=True
    )
    # El telefono SIMEPRE es un CharField!
    TELEFONO = models.CharField(max_length=200)
    CORREO = models.CharField(max_length=200, null=True, blank=True)
    TIPO_PAGO = models.CharField(max_length=200, choices=TIPOS_DE_PAGO, null=True)

    OBSERVACIONES = models.CharField(max_length=200, blank=True)

    def save(self, *args, **kwargs):
        self.NOMBRE = self.NOMBRE.upper()
        if self.CONTACTO:
            self.CONTACTO = self.CONTACTO.upper()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Delete the associated Direccion if it exists
        if self.DIRECCION:
            self.DIRECCION.delete()
        super().delete(*args, **kwargs)

    def __str__(self):
        return str(self.NOMBRE)


class PrecioCliente(models.Model):
    # Debido a que si se borrar cliente se debe de borrar el correspondiente precio(s). Aqui si tiene sentido usar el foreigkey y no solo el nombre del cliente. Los mismo para producto.
    CLIENTE = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, related_name="precios_cliente"
    )

    PRODUCTO = models.ForeignKey(Producto, on_delete=models.CASCADE)

    PRECIO = models.FloatField(validators=[MinValueValidator(0)])

    # En este metodo nunca debes de poner algo que se pueda volver None. Por ejemplo, en este caso estamos seguros de que CLIENTE y PRODUCTO siempre seran valores distintos de None
    def __str__(self):
        return f"{self.CLIENTE.NOMBRE}, {self.PRODUCTO.NOMBRE}, {self.PRECIO}"


class Venta(models.Model):
    VENDEDOR = models.CharField(max_length=100)

    # Creo que deberia cambia el foreigkey por un charfield
    # no necesito el cliente entero para registrar una venta, solo necesito su nombre
    # Ya lo puedo borrar (Lo voy a dejar por ahora, pero no lo necesito)
    CLIENTE = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)

    NOMBRE_CLIENTE = models.CharField(max_length=200)

    FECHA = models.DateTimeField(auto_now=True)

    MONTO = models.FloatField(validators=[MinValueValidator(0)])

    TIPO_VENTA = models.CharField(
        max_length=100, choices=(("MOSTRADOR", "MOSTRADOR"), ("RUTA", "RUTA"))
    )

    TIPO_PAGO = models.CharField(
        max_length=100,
        choices=(
            ("CONTADO", "CONTADO"),
            ("CREDITO", "CREDITO"),
            ("CORTESIA", "CORTESIA"),
        ),
    )

    STATUS = models.CharField(
        max_length=100,
        choices=(
            ("REALIZADO", "REALIZADO"),
            ("PENDIENTE", "PENDIENTE"),
            ("CANCELADO", "CANCELADO"),
        ),
    )

    OBSERVACIONES = models.CharField(max_length=100, blank=True)

    DESCUENTO = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f"{self.TIPO_VENTA}, {self.MONTO}, {self.TIPO_PAGO}"


class ProductoVenta(models.Model):
    VENTA = models.ForeignKey(
        Venta, on_delete=models.CASCADE, related_name="productos_venta"
    )
    # Tampoco necesito el id del producto, solo su nombre. En realidad no es tan importante dejar o no esta relacion. Lo que importa es que hacer cuando un producto es eliminado, en este caso el producto venta permanece con producto igual a null.
    # Una razon para usar el id y no el nombre al momento de registrar el producto venta, es si es importante actualizar el producto venta cuando el producto es actualizado, por ejemplo, cambiar el nombre.
    PRODUCTO = models.ForeignKey(Producto, on_delete=models.SET_NULL, null=True)
    NOMBRE_PRODUCTO = models.CharField(max_length=200)

    CANTIDAD_VENTA = models.FloatField(validators=[MinValueValidator(0)])
    PRECIO_VENTA = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.VENTA}, {self.NOMBRE_PRODUCTO}"
