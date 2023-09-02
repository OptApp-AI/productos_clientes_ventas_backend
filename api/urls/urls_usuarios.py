from django.urls import path
from api.views import views_usuarios

urlpatterns = [
    path("usuarios/", views_usuarios.usuario_list),
    path("usuarios/<str:pk>/", views_usuarios.usuario_detail),
    path("crear-cuenta/", views_usuarios.crear_user),
    path("modificar-usuario/<str:pk>/", views_usuarios.modificar_usuario),
]
