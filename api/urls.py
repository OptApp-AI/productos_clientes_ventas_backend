from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [

    # Cuenta
    # path('crear-user/', views.crear_user),
    path('cuenta-detalles/', views.cuenta_detail),
    path('modificar-cuenta/', views.modificar_cuenta),

    # Borrar cuenta

    # Usuarios
    path('usuarios/', views.usuario_list),
    path('usuarios/<str:pk>/', views.usuario_detail),
    path('crear-cuenta/', views.crear_user),
    path("modificar-usuario/<str:pk>/", views.modificar_usuario),

    # Productos
    path("productos/", views.producto_list),
    path("crear-producto/", views.crear_producto),
    path("productos/<str:pk>/", views.producto_detail),
    path("modificar-producto/<str:pk>/", views.modificar_producto),

    # Clientes 
    path("clientes/", views.cliente_list),
    path("crear-cliente/", views.crear_cliente),
    path("clientes/<str:pk>/", views.cliente_detail),
    path("modificar-cliente/<str:pk>/", views.modificar_cliente),

    # Ventas 
    path("ventas/", views.venta_list), 
    path("crear-venta/", views.crear_venta),
    path("ventas/<str:pk>/", views.venta_detail),
    path("modificar-venta/<str:pk>/", views.modificar_venta),

    # Login
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]