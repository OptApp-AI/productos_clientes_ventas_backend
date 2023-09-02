from django.urls import path
from api.views import views_productos


urlpatterns = [
    path("productos/", views_productos.producto_list),
    path("crear-producto/", views_productos.crear_producto),
    path("productos/<str:pk>/", views_productos.producto_detail),
    path("modificar-producto/<str:pk>/", views_productos.modificar_producto),
]
