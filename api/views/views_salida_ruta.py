from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from api.models import (
    SalidaRuta,
    ProductoSalidaRuta,
    ClienteSalidaRuta,
    Cliente,
    Producto,
    RutaDia,
)
from api.serializers import SalidaRutaSerializer


@api_view(["GET"])
def salida_ruta_list(request):
    queryset = SalidaRuta.objects.all()

    serializer = SalidaRutaSerializer(queryset, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def salida_ruta_detail(request, pk):
    try:
        salida_ruta = SalidaRuta.objects.get(pk=pk)
    except SalidaRuta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SalidaRutaSerializer(salida_ruta)

    return Response(serializer.data)


@api_view(["POST"])
def crear_salida_ruta(request):
    data = request.data

    ruta_dia = RutaDia.objects.get(RUTA=data.get("rutaId"), DIA=data.get("DIA"))

    print("Ruta Dia", ruta_dia, data.get("rutaId"), data.get("DIA"))
    data["RUTA"] = ruta_dia.id

    serializer = SalidaRutaSerializer(data=data)

    if serializer.is_valid():
        salida_ruta = serializer.save()

        # Generar ProductoSalidaRuta
        salida_ruta_productos = data["salidaRutaProductos"]

        for salida_ruta_producto in salida_ruta_productos:
            producto = Producto.objects.get(pk=salida_ruta_producto["productoId"])

            producto_salida_ruta = ProductoSalidaRuta.objects.create(
                SALIDA_RUTA=salida_ruta,
                PRODUCTO_RUTA=producto,
                CANTIDAD_RUTA=salida_ruta_producto["cantidadSalidaRuta"],
                CANTIDAD_DISPONIBLE=salida_ruta_producto["cantidadSalidaRuta"],
                STATUS="CARGADO",
            )

            producto.CANTIDAD -= producto_salida_ruta.CANTIDAD_RUTA
            producto.save()
            producto_salida_ruta.save()

        # Genrar ClienteSalidaRuta
        salida_ruta_clientes = data["salidaRutaClientes"]

        for salida_ruta_cliente in salida_ruta_clientes:
            cliente_salida_ruta = ClienteSalidaRuta.objects.create(
                SALIDA_RUTA=salida_ruta,
                CLIENTE_RUTA=Cliente.objects.get(id=salida_ruta_cliente["clienteId"]),
                STATUS="PENDIENTE",
            )

            cliente_salida_ruta.save()

        return Response(serializer.data)
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
