from django.urls import path
from api.views import views_clientes

urlpatterns = [
    path("clientes/", views_clientes.cliente_list),
    path(
        "clientes-venta/", views_clientes.cliente_venta_lista
    ),  # para realizar la venta necesitamos tener accesso a cualquier cliente, no solo los que se regresan en una pagina
    path("crear-cliente/", views_clientes.crear_cliente),
    path("clientes/<str:pk>/", views_clientes.cliente_detail),
    path("modificar-cliente/<str:pk>/", views_clientes.modificar_cliente),
    # Ruta
    path("rutas/", views_clientes.ruta_list),
    path("crear-ruta/", views_clientes.crear_ruta),
    path("rutas/<str:pk>/", views_clientes.ruta_detail),
    path("modificar-ruta/<str:pk>/", views_clientes.modificar_ruta),
]
