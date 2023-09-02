from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import (
    Producto,
    Cliente,
    PrecioCliente,
    Direccion,
)
from api.serializers import (
    ClienteSerializer,
    ClienteVentaSerializer,
)
from django.db.models import Case, When, Value, IntegerField
from django.db.models import Case, When, Value, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@api_view(["GET"])
def cliente_list(request):
    # 1. Filtrar usando parametro clientfiltrarpor
    filtrar_por = request.GET.get("clientefiltrarpor", "")
    buscar = request.GET.get("clientebuscar", "")

    if filtrar_por == "nombre" and buscar:
        queryset = Cliente.objects.filter(NOMBRE__icontains=buscar)
    elif filtrar_por == "contacto":
        queryset = Cliente.objects.filter(CONTACTO__icontains=buscar)
    elif filtrar_por == "tipopago":
        queryset = Cliente.objects.filter(TIPO_PAGO__icontains=buscar)
    else:
        queryset = Cliente.objects.all()

    # 2. Ordenar usando clienteordenarpor
    ordenar_por = request.GET.get("clienteordenarpor", "")

    if ordenar_por == "nombre":
        queryset = queryset.order_by("NOMBRE")
    elif ordenar_por == "contacto":
        # Primero ordenamos de tal forma que los clientes
        # con contacto distinto de '' esten al inicio
        # Luego, como segundo criterio ordenamos con respecto al nombre del contacto
        queryset = queryset.annotate(
            is_empty=Case(
                When(CONTACTO="", then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by("is_empty", "CONTACTO")
    else:
        queryset = queryset.order_by("-id")

    # 3. Paginacion
    page = request.GET.get("page")
    paginator = Paginator(queryset, 5)

    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        clientes = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        clientes = paginator.page(page)

    serializer = ClienteSerializer(clientes, many=True)

    return Response(
        {"clientes": serializer.data, "page": page, "pages": paginator.num_pages},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
def cliente_venta_lista(request):
    queryset = Cliente.objects.all()

    serializer = ClienteVentaSerializer(queryset, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def crear_cliente(request):
    data = request.data

    # 1. Crear cliente
    serializer = ClienteSerializer(data=data)

    if serializer.is_valid():
        cliente = serializer.save()

        # 2. Crear precios del cliente
        precios_cliente = data["preciosCliente"]
        for precio_cliente in precios_cliente:
            nuevo_precio_cliente = PrecioCliente.objects.create(
                CLIENTE=cliente,
                PRODUCTO=Producto.objects.get(pk=precio_cliente["productoId"]),
                PRECIO=precio_cliente["precioCliente"],
            )

            nuevo_precio_cliente.save()

        # 3. Crear direccion
        direccion = data["direccion"]

        nueva_direccion = Direccion.objects.create(**direccion)

        nueva_direccion.save()

        cliente.DIRECCION = nueva_direccion

        cliente.save()

        # Es importante tener en cuenta que, aunque creas los objetos PrecioCliente después de haber validado y serializado el objeto Cliente, estos objetos estarán disponibles en la instancia del objeto Cliente y se incluirán en la respuesta cuando se serialice el objeto Cliente utilizando el serializer ClienteSerializer.
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def cliente_detail(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response(
            {"message": "Cliente con el id dado no existe"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = ClienteSerializer(cliente)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PUT", "DELETE"])
def modificar_cliente(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response(
            {"message": "Cliente con el id dado no existe"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if request.method == "PUT":
        data = request.data
        # 1. Actualizar cliente
        serializer = ClienteSerializer(cliente, data=data)

        if serializer.is_valid():
            serializer.save()

            # 2. Modificar el precio de los clientes
            nuevos_precios_cliente = data["nuevosPreciosCliente"]

            for nuevo_precio_cliente in nuevos_precios_cliente:
                precioCliente = PrecioCliente.objects.get(
                    pk=nuevo_precio_cliente["precioClienteId"]
                )
                precioCliente.PRECIO = nuevo_precio_cliente["nuevoPrecioCliente"]
                precioCliente.save()

            # 3. Modificar la direccion
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

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        cliente.delete()

        return Response(
            {"message": "Cliente fue eliminado exitosamente"},
            status=status.HTTP_204_NO_CONTENT,
        )
