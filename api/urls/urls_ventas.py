from django.urls import path
from api.views import views_ventas

urlpatterns = [
    path("ventas/", views_ventas.venta_list),
    path(
        "ventas-reporte/", views_ventas.venta_reporte_list
    ),  # para generar el reporte necesitamos todas las venta. no una sola pagina
    path("crear-venta/", views_ventas.crear_venta),
    path("ventas/<str:pk>/", views_ventas.venta_detail),
    path("modificar-venta/<str:pk>/", views_ventas.modificar_venta),
]
