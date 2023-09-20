from django.contrib import admin
from .models import (
    Producto,
    Cliente,
    PrecioCliente,
    Venta,
    ProductoVenta,
    Direccion,
    Empleado,
    # Rutas
    Ruta,
    SalidaRuta,
    ClienteSalidaRuta,
    ProductoSalidaRuta,
)


# Register your models here.


class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ("USUARIO",)


admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(PrecioCliente)
admin.site.register(Venta)
admin.site.register(ProductoVenta)
admin.site.register(Direccion)
admin.site.register(Empleado, EmpleadoAdmin)

# Ruta
admin.site.register(Ruta)
admin.site.register(SalidaRuta)
admin.site.register(ClienteSalidaRuta)
admin.site.register(ProductoSalidaRuta)
