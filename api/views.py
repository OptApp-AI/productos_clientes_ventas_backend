from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import (
    Producto,
    Cliente,
    PrecioCliente,
    Venta,
    ProductoVenta,
    Direccion,
    Empleado,
)
from .serializers import (
    ProductoSerializer,
    ClienteSerializer,
    VentaSerializer,
    ProductoVentaSerializer,
    UserSerializer,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
import sys


@api_view(["GET"])
def cuenta_detail(request):
    # the first line of code retrieves the User object associated with the current request by accessing the user attribute of the request object. The request.user attribute is automatically populated by Django's authentication middleware, which verifies the user's credentials based on the authentication backend that is configured in the Django settings.
    user = request.user

    serializer = UserSerializer(user)

    return Response(serializer.data)


@api_view(["PUT"])
def modificar_cuenta(request):
    user = request.user

    if isinstance(user, AnonymousUser):
        return Response(
            {"Detalles": "Necesitar autenticarte para modificar tu usuario"}
        )

    data = request.data
    password = data.get("password")
    imagen = data.get("IMAGEN")

    try:
        user.username = data["username"]
        if password:
            user.password = make_password(password)
        user.first_name = data["name"].upper()
        user.is_staff = True if data["is_admin"] == "true" else False

        user.save()

        if imagen:
            empleado = user.empleado
            empleado.IMAGEN = data["IMAGEN"]
            empleado.save()

        serializer = UserSerializer(user)
        return Response(serializer.data)

    except:
        return Response(
            {"Detalles": "Un usuario con este username ya existe"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def crear_user(request):
    data = request.data

    if data["password1"] != data["password2"]:
        return Response(
            {"Detalles": "Las constraseñas deben ser iguales"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        user = User.objects.create(
            username=data["username"],
            password=make_password(data["password1"]),
            first_name=data["name"].upper(),
            is_staff=True if data["is_admin"] == "true" else False,
        )

        if data.get("IMAGEN"):
            Empleado.objects.create(
                USUARIO=user,
                IMAGEN=data["IMAGEN"],
            )
        else:
            Empleado.objects.create(USUARIO=user)

        serializer = UserSerializer(user)
        return Response(serializer.data)

    except Exception as e:
        # print("Error:", str(e))
        # print("Detalles del error:", sys.exc_info())
        return Response(
            {"Detalles": "Un usuario con este username ya existe"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["GET"])
def usuario_list(request):
    queryset = User.objects.all()

    serializer = UserSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def usuario_detail(request, pk):
    try:
        usuario = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(
            {"Detalles": "El usuario no existe"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = UserSerializer(usuario)
    return Response(serializer.data)


@api_view(["PUT", "DELETE"])
def modificar_usuario(request, pk):
    data = request.data
    try:
        usuario = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        usuario.is_staff = True if data["is_admin"] == "true" else False
        usuario.save()

        serializer = UserSerializer(usuario)

        return Response(serializer.data)

    if request.method == "DELETE":
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username

    #     return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializer(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Vistas para productos
@api_view(["GET"])
def producto_list(request):
    queryset = Producto.objects.all()

    serializer = ProductoSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def crear_producto(request):
    serializer = ProductoSerializer(data=request.data)

    if serializer.is_valid():
        producto = serializer.save()

        queryset = Cliente.objects.all()

        clientes_serializer = ClienteSerializer(queryset, many=True)

        for cliente_serializer in clientes_serializer.data:
            precio_cliente = PrecioCliente.objects.create(
                CLIENTE=Cliente.objects.get(pk=cliente_serializer["id"]),
                PRODUCTO=producto,
                PRECIO=producto.PRECIO,
            )

            precio_cliente.save()

        return Response(serializer.data)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def producto_detail(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ProductoSerializer(producto)
    return Response(serializer.data)


@api_view(["PUT", "DELETE"])
def modificar_producto(request, pk):
    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Vistas para clientes
@api_view(["GET"])
def cliente_list(request):
    queryset = Cliente.objects.all()

    page = request.query_params.get("page")

    paginator = Paginator(queryset, 10)

    try:
        clientes = paginator.page(page)

    except PageNotAnInteger:
        clientes = paginator.page(1)

    except EmptyPage:
        clientes = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = ClienteSerializer(clientes, many=True)

    return Response(
        {"clientes": serializer.data, "page": page, "pages": paginator.num_pages}
    )

    serializer = ClienteSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(["POST"])
def crear_cliente(request):
    data = request.data

    # Crear cliente
    serializer = ClienteSerializer(data=data)

    if serializer.is_valid():
        cliente = serializer.save()

        # Crear precios
        precios_cliente = data["preciosCliente"]
        for precio_cliente in precios_cliente:
            nuevo_precio_cliente = PrecioCliente.objects.create(
                CLIENTE=cliente,
                PRODUCTO=Producto.objects.get(pk=precio_cliente["productoId"]),
                PRECIO=precio_cliente["precioCliente"],
            )

            nuevo_precio_cliente.save()

        # Crear direccion
        direccion = data["direccion"]

        nueva_direccion = Direccion.objects.create(**direccion)

        nueva_direccion.save()

        cliente.DIRECCION = nueva_direccion

        cliente.save()

        # Por lo tanto, es importante tener en cuenta que, aunque creas los objetos PrecioCliente después de haber validado y serializado el objeto Cliente, estos objetos estarán disponibles en la instancia del objeto Cliente y se incluirán en la respuesta cuando se serialice el objeto Cliente utilizando el serializer ClienteSerializer.
        return Response(serializer.data)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def cliente_detail(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ClienteSerializer(cliente)
    return Response(serializer.data)


@api_view(["PUT", "DELETE"])
def modificar_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        data = request.data

        serializer = ClienteSerializer(cliente, data=data)

        if serializer.is_valid():
            serializer.save()

            # Modificar el precio de los clientes
            nuevos_precios_cliente = data["nuevosPreciosCliente"]

            for nuevo_precio_cliente in nuevos_precios_cliente:
                precioCliente = PrecioCliente.objects.get(
                    pk=nuevo_precio_cliente["precioClienteId"]
                )
                precioCliente.PRECIO = nuevo_precio_cliente["nuevoPrecioCliente"]
                precioCliente.save()

            # Modificar la direccion
            nueva_direccion = data["nuevaDireccion"]

            direccionCliente = Direccion.objects.get(
                pk=nueva_direccion["direccionClienteId"]
            )

            direccionCliente.CALLE = nueva_direccion["CALLE"]
            direccionCliente.NUMERO = nueva_direccion["NUMERO"]
            direccionCliente.COLONIA = nueva_direccion["COLONIA"]
            direccionCliente.CIUDAD = nueva_direccion["CIUDAD"]
            direccionCliente.MUNICIPIO = nueva_direccion["MUNICIPIO"]
            direccionCliente.CP = nueva_direccion["CP"]

            direccionCliente.save()

            return Response(serializer.data)
        return Response(serializer.errors)

    elif request.method == "DELETE":
        cliente.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# Vistas para ventas
@api_view(["GET"])
def venta_list(request):
    queryset = Venta.objects.all().order_by("-FECHA")

    page = request.query_params.get("page")

    paginator = Paginator(queryset, 10)

    try:
        ventas = paginator.page(page)

    except PageNotAnInteger:
        ventas = paginator.page(1)

    except EmptyPage:
        ventas = paginator.page(paginator.num_pages)

    if page == None:
        page = 1

    page = int(page)

    serializer = VentaSerializer(ventas, many=True)

    return Response(
        {"ventas": serializer.data, "page": page, "pages": paginator.num_pages}
    )


@api_view(["POST"])
def crear_venta(request):
    data = request.data

    serializer = VentaSerializer(data=data)

    if serializer.is_valid():
        venta = serializer.save()

        productos_venta = data["productosVenta"]

        for producto_venta in productos_venta:
            producto = Producto.objects.get(pk=producto_venta["productoId"])

            nuevo_producto_venta = ProductoVenta.objects.create(
                VENTA=venta,
                PRODUCTO=producto,
                CANTIDAD_VENTA=producto_venta["cantidadVenta"],
                PRECIO_VENTA=producto_venta["precioVenta"],
            )

            if data["STATUS"] == "REALIZADO":
                producto.CANTIDAD -= nuevo_producto_venta.CANTIDAD_VENTA
                producto.save()

            nuevo_producto_venta.save()

        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(["GET"])
def venta_detail(request, pk):
    try:
        venta = Venta.objects.get(pk=pk)

    except Venta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = VentaSerializer(venta)
    return Response(serializer.data)


@api_view(["PUT", "DELETE"])
def modificar_venta(request, pk):
    try:
        venta = Venta.objects.get(pk=pk)

    except Venta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "PUT":
        reporte_cambios = {}

        data = request.data

        status_actual = venta.STATUS
        status_cambios = {"ANTES": status_actual}

        status_nuevo = data["STATUS"]

        productos_venta = venta.productos_venta

        serializer = ProductoVentaSerializer(productos_venta, many=True)

        for producto_venta_serializer in serializer.data:
            producto = Producto.objects.get(
                NOMBRE=producto_venta_serializer["producto_nombre"]
            )

            producto_cambios = {"ANTES": producto.CANTIDAD}

            cantidad_venta = producto_venta_serializer["CANTIDAD_VENTA"]

            producto.CANTIDAD = calcular_cantidad(
                status_actual, status_nuevo, producto.CANTIDAD, cantidad_venta
            )
            producto.save()
            producto_cambios["DESPUES"] = producto.CANTIDAD

            reporte_cambios[producto.NOMBRE] = producto_cambios

        venta.STATUS = status_nuevo
        venta.save()
        status_cambios["DESPUES"] = venta.STATUS
        reporte_cambios["STATUS"] = status_cambios

        return Response(reporte_cambios)

    elif request.method == "DELETE":
        venta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def calcular_cantidad(status_actual, status, cantidad_antes, cantidad_venta):
    if status_actual == "PENDIENTE":
        if status == "REALIZADO":
            return cantidad_antes - cantidad_venta
        else:
            return cantidad_antes
    elif status_actual == "REALIZADO":
        if status in ["PENDIENTE", "CANCELADO"]:
            return cantidad_antes + cantidad_venta
        else:
            return cantidad_antes
    else:
        return cantidad_antes
