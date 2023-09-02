from django.urls import path
from api.views import views_cuenta


urlpatterns = [
    # path("cuenta-detalles/", views_cuenta.cuenta_detail),
    path("modificar-cuenta/", views_cuenta.modificar_cuenta),
]
