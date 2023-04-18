from rest_framework import serializers
from .models import Producto, Cliente, PrecioCliente, ProductoVenta, Venta, Direccion, Empleado
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class EmpleadoSerializer(serializers.ModelSerializer):

    class Meta: 
        model = Empleado
        fields = ('IMAGEN', )

class UserSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField(read_only=True)
    is_admin = serializers.SerializerMethodField(read_only=True)

    empleado = EmpleadoSerializer()

    class Meta: 
        model = User 
        fields = ('id','username', 'name', 'is_admin', 'empleado')

    def get_name(self,obj):
        name = obj.first_name
        if not name:
            name = obj.username 
        return name 
    
    def get_is_admin(self, obj):
        is_admin = obj.is_staff
        return is_admin

# class UserSerializerWithToken(UserSerializer):
#     token = serializers.SerializerMethodField(read_only=True)


#     class Meta:
#         model= User 
#         fields = ('id','username', 'name', 'is_admin', 'token')

#     def get_token(sefl, obj):
#         token = RefreshToken.for_user(obj)
#         return str(token.access_token)



class DireccionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Direccion
        fields = '__all__'


class ProductoSerializer(serializers.ModelSerializer):


    class Meta:
        model = Producto
        fields = '__all__'


class PrecioClienteSerializer(serializers.ModelSerializer): 

    producto_nombre = serializers.CharField(source='PRODUCTO.NOMBRE', read_only=True)

    producto_cantidad = serializers.IntegerField(source='PRODUCTO.CANTIDAD', read_only=True)

    class Meta:
        model = PrecioCliente
        fields = "__all__"


class ClienteSerializer(serializers.ModelSerializer):

    precios_cliente = PrecioClienteSerializer(many=True, read_only=True)


    DIRECCION = DireccionSerializer(required=False)

    class Meta:
        model = Cliente
        fields = '__all__'
    

class ProductoVentaSerializer(serializers.ModelSerializer):

    producto_nombre = serializers.CharField(source='PRODUCTO.NOMBRE', read_only=True)

    class Meta:

        model = ProductoVenta
        fields = "__all__"

class VentaSerializer(serializers.ModelSerializer):

    productos_venta = ProductoVentaSerializer(many=True, read_only=True)

    cliente_nombre = serializers.CharField(source='CLIENTE.NOMBRE', read_only=True)

    class Meta:

        model = Venta
        fields = "__all__"


