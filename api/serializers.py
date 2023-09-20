from rest_framework import serializers
from .models import (
    Producto,
    Cliente,
    PrecioCliente,
    ProductoVenta,
    Venta,
    Direccion,
    Empleado,
    # Ruta
    Ruta,
)
from django.contrib.auth.models import User


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = ("IMAGEN",)


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    # Algo mas sencillo aqui seria crear el campo imagen  en el serializerusando empleado para ello, de esta manera, accedes a image desde usuario y no necesitar usar empleado en el frontend
    empleado = EmpleadoSerializer()

    class Meta:
        model = User
        fields = ("id", "username", "name", "is_admin", "empleado")

    def get_name(self, obj):
        name = obj.first_name
        if not name:
            name = obj.username
        return name

    def get_is_admin(self, obj):
        is_admin = obj.is_staff
        return is_admin


class DireccionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direccion
        fields = "__all__"


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = "__all__"


class PrecioClienteSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(source="PRODUCTO.NOMBRE", read_only=True)

    # La cantidad es para poder hacer una venta a este cliente, sabiendo cuantos productos tengo disponibles

    # Pero esto solo es necesario cuando realizo una venta, no cuando quiero ver informacion del cliente
    producto_cantidad = serializers.IntegerField(
        source="PRODUCTO.CANTIDAD", read_only=True
    )

    # La imagen es para el momento de hacer la venta
    # Los mismo que dije antes, esto solo es necesario al momento de hacer una venta
    producto_imagen = serializers.ImageField(source="PRODUCTO.IMAGEN", read_only=True)

    porcentage_precio = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PrecioCliente
        fields = "__all__"
        # fields = ("id", "PRECIO", "producto_nombre")

    def get_porcentage_precio(self, obj):
        precio_publico = obj.PRODUCTO.PRECIO if obj.PRODUCTO.PRECIO else 1
        precio_cliente = obj.PRECIO if obj.PRECIO else 0

        if precio_publico == 0:
            return "NO DISPONIBLE"

        descuento = (1 - (precio_cliente / precio_publico)) * 100

        return round(descuento, 2)


class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = "__all__"


class ClienteSerializer(serializers.ModelSerializer):
    # Debo cambia el serializador de precios, remover producto_cantidad,  producto_imagen
    precios_cliente = PrecioClienteSerializer(many=True, read_only=True)

    DIRECCION = DireccionSerializer(required=False)

    RUTAS = RutaSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = "__all__"


class ClienteVentaSerializer(serializers.ModelSerializer):
    # Debo cambia el serializador de precios, remover porcentage_precio
    precios_cliente = PrecioClienteSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = ("id", "precios_cliente", "NOMBRE")


class ProductoVentaSerializer(serializers.ModelSerializer):
    # producto_nombre = serializers.CharField(source="PRODUCTO.NOMBRE", read_only=True)

    class Meta:
        model = ProductoVenta
        fields = "__all__"
        # fiels = ("id", "NOMBRE_PRODUCTO") Quiza esto es mejor para el rendimiento


class VentaSerializer(serializers.ModelSerializer):
    productos_venta = ProductoVentaSerializer(many=True, read_only=True)

    # cliente_nombre = serializers.CharField(source="CLIENTE.NOMBRE", read_only=True)

    class Meta:
        model = Venta
        fields = "__all__"
