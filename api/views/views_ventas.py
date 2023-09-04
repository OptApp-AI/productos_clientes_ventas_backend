from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from api.models import (
    Producto,
    Venta,
    ProductoVenta,
)
from api.serializers import (
    VentaSerializer,
    ProductoVentaSerializer,
)
from django.db.models import Case, When, Value, IntegerField
from django.utils.dateparse import parse_date
from django.db.models import Case, When, Value, IntegerField
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta


# Vistas para ventas
@api_view(["GET"])
def venta_list(request):
    # 1. Filtrar usando parametro filtrarpor
    filtrar_por = request.GET.get("filtrarpor", "")
    buscar = request.GET.get("buscar", "")

    # No es posible que exista buscar y no exista filtrar_por
    # pero puede existir filtrar_por = "clientes" y buscar ser ''

    if filtrar_por == "cliente" and buscar:
        queryset = Venta.objects.filter(NOMBRE_CLIENTE__icontains=buscar)
    elif filtrar_por == "tipoventa":
        queryset = Venta.objects.filter(TIPO_VENTA__icontains=buscar)
    elif filtrar_por == "tipopago":
        queryset = Venta.objects.filter(TIPO_PAGO__icontains=buscar)
    elif filtrar_por == "status":
        queryset = Venta.objects.filter(STATUS__icontains=buscar)

    elif filtrar_por == "vendedor":
        queryset = Venta.objects.filter(VENDEDOR__icontains=buscar)
    else:
        queryset = Venta.objects.all()

    # 2. Filtrar por fecha
    fechainicio = request.GET.get("fechainicio", "")
    fechafinal = request.GET.get("fechafinal", "")
    if fechainicio:
        fechainicio = parse_date(fechainicio)
    if fechafinal:
        # El timedelta es para que el filtro incluya el dia actual cuando fechFinal es el dia actual
        fechafinal = parse_date(fechafinal) + timedelta(days=1)
    if fechainicio and fechafinal:
        queryset = queryset.filter(FECHA__date__range=[fechainicio, fechafinal])
    elif fechainicio:
        queryset = queryset.filter(FECHA__date__gte=fechainicio)
    elif fechafinal:
        queryset = queryset.filter(FECHA__date__lte=fechafinal)

    # 3. Ordenar usando ordenarpor
    ordenar_por = request.GET.get("ordernarpor", "")

    # Primero ordenamos de tal forma que las ventas
    # con cliente estan al inicio
    # Luego, como segundo criterio ornamos con recpecto al nombre del cliente
    if ordenar_por == "cliente":
        queryset = queryset.order_by("NOMBRE_CLIENTE")

    elif ordenar_por == "fecha_recientes":
        queryset = queryset.order_by("-FECHA")

    elif ordenar_por == "fecha_antiguos":
        queryset = queryset.order_by("FECHA")

    elif ordenar_por == "vendedor":
        queryset = queryset.order_by("VENDEDOR")
    else:
        queryset = queryset.order_by("-id")

    # 4. Paginacion
    page = request.GET.get("page")

    paginator = Paginator(queryset, 10)

    try:
        ventas = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        ventas = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        ventas = paginator.page(page)

    serializer = VentaSerializer(ventas, many=True)

    return Response(
        {"ventas": serializer.data, "page": page, "pages": paginator.num_pages},
        status=status.HTTP_200_OK,
    )


# Vistas para ventas
@api_view(["GET"])
def venta_reporte_list(request):
    # 1. Filtrar usando parametro filtrarpor
    filtrar_por = request.GET.get("filtrarpor", "")
    buscar = request.GET.get("buscar", "")

    if filtrar_por == "cliente" and buscar:
        queryset = Venta.objects.filter(NOMBRE_CLIENTE__icontains=buscar)
    elif filtrar_por == "tipoventa":
        queryset = Venta.objects.filter(TIPO_VENTA__icontains=buscar)
    elif filtrar_por == "tipopago":
        queryset = Venta.objects.filter(TIPO_PAGO__icontains=buscar)
    elif filtrar_por == "status":
        queryset = Venta.objects.filter(STATUS__icontains=buscar)

    elif filtrar_por == "vendedor":
        queryset = Venta.objects.filter(VENDEDOR__icontains=buscar)
    else:
        queryset = Venta.objects.all()

    # 2. Filtrar por fecha
    fechainicio = request.GET.get("fechainicio", "")
    fechafinal = request.GET.get("fechafinal", "")
    if fechainicio:
        fechainicio = parse_date(fechainicio)
    if fechafinal:
        fechafinal = parse_date(fechafinal) + timedelta(days=1)
    if fechainicio and fechafinal:
        queryset = queryset.filter(FECHA__date__range=[fechainicio, fechafinal])
    elif fechainicio:
        queryset = queryset.filter(FECHA__date__gte=fechainicio)
    elif fechafinal:
        queryset = queryset.filter(FECHA__date__lte=fechafinal)

    # 3. Ordenar usando ordenarpor
    ordenar_por = request.GET.get("ordernarpor", "")

    if ordenar_por == "cliente":
        queryset = queryset.order_by("NOMBRE_CLIENTE")

    elif ordenar_por == "fecha_recientes":
        queryset = queryset.order_by("-FECHA")

    elif ordenar_por == "fecha_antiguos":
        queryset = queryset.order_by("FECHA")

    elif ordenar_por == "vendedor":
        queryset = queryset.order_by("VENDEDOR")
    else:
        queryset = queryset.order_by("-id")

    serializer = VentaSerializer(queryset, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


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
                NOMBRE_PRODUCTO=producto.NOMBRE,
                CANTIDAD_VENTA=producto_venta["cantidadVenta"],
                PRECIO_VENTA=producto_venta["precioVenta"],
            )

            if data["STATUS"] == "REALIZADO":
                producto.CANTIDAD -= nuevo_producto_venta.CANTIDAD_VENTA
                producto.save()

            nuevo_producto_venta.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    print("ERRORES:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                NOMBRE=producto_venta_serializer["NOMBRE_PRODUCTO"]
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
