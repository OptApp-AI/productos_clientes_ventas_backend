from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

class Empleado(models.Model): 

    USUARIO = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True) 

    IMAGEN = models.ImageField(default='imagenes/empleados/user-default.png', upload_to='imagenes/empleados')

    def __str__(self):
        return f'{self.USUARIO.first_name}, {self.IMAGEN}'



# Create your models here.
class Producto(models.Model):

    NOMBRE = models.CharField(max_length=100)

    CANTIDAD = models.FloatField(validators=[MinValueValidator(0)])

    PRECIO = models.FloatField(validators=[MinValueValidator(0)])

    IMAGEN = models.ImageField(default='imagenes/producto_default.jpg', upload_to='imagenes')

    # RECUERDA NO PONER NADA QUE SE PUEDE VOLVER NULL AQUI
    def __str__(self):
        return f"{self.NOMBRE}, {self.CANTIDAD}, {self.PRECIO}"

class Direccion(models.Model): 

    CALLE = models.CharField(max_length=200)
    NUMERO = models.IntegerField(validators=[
        MinValueValidator(0)
    ])
    COLONIA = models.CharField(max_length=200, null=True, blank=True)
    CIUDAD = models.CharField(max_length=200)
    MUNICIPIO = models.CharField(max_length=200, null=True, blank=True)
    CP = models.IntegerField(validators=[
        MinValueValidator(0)
    ], null=True, blank=True)

    class Meta:

        verbose_name_plural = 'Direcciones'

    def __str__(self):
        return f'{self.CALLE}, {self.NUMERO}, {self.COLONIA}'

class Cliente(models.Model):

    TIPOS_DE_PAGO = (
        ('EFECTIVO', 'EFECTIVO'),
        ('CREDITO', 'CREDITO'),
    )

    NOMBRE = models.CharField(max_length=200)

    CONTACTO = models.CharField(max_length=200, null=True)

    DIRECCION = models.OneToOneField(Direccion, on_delete=models.SET_NULL, null=True, blank=True)

    TELEFONO = models.IntegerField(validators=[MinValueValidator(0)], null=True, unique=True)
    CORREO = models.CharField(max_length=200, null=True, unique=True)
    TIPO_PAGO = models.CharField(max_length=200, choices=TIPOS_DE_PAGO, null=True)

    def clean(self):

        # obtener clientes con nombre y telefono
        clientes_existentes = Cliente.objects.filter(models.Q(CORREO=self.CORREO) | models.Q(TELEFONO = self.TELEFONO)).exclude(id=self.id)

        # crea una lista de mensajes de error a mostrar al usuario

        mensajes_error = []

        if clientes_existentes.exists():

            if clientes_existentes.filter(CORREO=self.CORREO).exists():
                mensajes_error.append('Un cliente con este correo ya existe.')

            if clientes_existentes.filter(TELEFONO=self.TELEFONO).exists():
                mensajes_error.append('Un cliente con este teléfono ya existe.')

            raise ValidationError(mensajes_error)
        
    def __str__(self):
        return str(self.NOMBRE)
    
class PrecioCliente(models.Model):

    CLIENTE = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="precios_cliente") 

    PRODUCTO = models.ForeignKey(Producto, on_delete=models.CASCADE)

    PRECIO = models.FloatField(validators=[MinValueValidator(0)])


    def __str__(self):
        return f"{self.CLIENTE.NOMBRE}, {self.PRODUCTO.NOMBRE}, {self.PRECIO}"


class Venta(models.Model):

    VENDEDOR = models.CharField(max_length=100)

    CLIENTE = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)

    FECHA = models.DateTimeField(auto_now=True)

    MONTO = models.FloatField(validators=[MinValueValidator(0)])

    TIPO_VENTA =  models.CharField(max_length=100, choices=(("MOSTRADOR", "MOSTRADOR"), ("RUTA", "RUTA")))

    TIPO_PAGO = models.CharField(max_length=100, choices=(("CONTADO", "CONTADO"), ("CREDITO", "CREDITO"), ("CORTESIA", "CORTESIA")))

    STATUS = models.CharField(max_length=100, choices=(("REALIZADO", "REALIZADO"), ("PENDIENTE", "PENDIENTE"), ("CANCELADO", "CANCELADO")))

    OBSERVACIONES = models.CharField(max_length=100)

    DESCUENTO = models.FloatField(validators=[
        MinValueValidator(0), MaxValueValidator(100)
    ], null=True, blank=True)

    def __str__(self):
        return f"{self.TIPO_VENTA}, {self.MONTO}, {self.TIPO_PAGO}"


class ProductoVenta(models.Model):

    VENTA = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="productos_venta")
    PRODUCTO = models.ForeignKey(Producto, on_delete=models.CASCADE)
    CANTIDAD_VENTA = models.FloatField(validators=[MinValueValidator(0)])
    PRECIO_VENTA = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.VENTA}, {self.PRODUCTO.NOMBRE}"

